import discord
import asyncpraw, asyncprawcore
import requests
import io
import re
import asyncio
import datetime

import keys

import warnings
warnings.filterwarnings('ignore')

class reddit:
    help = {"list": True, "ListPriority": 5, "Title":"Reddit",
        "ShortHelp": "Get a post from a subreddit.",
        "LongHelp": "Get a post from a subreddit.\n"+
        "**@{displayName} reddit** to get a post from the front page.\n"+
        "**@{displayName} reddit r/<subreddit>** or **@{displayName} r/<subreddit>** "+
        "to get a post from the front page of that subreddit.\n"+
        "**@{displayName} reddit r/<subreddit> [hot/top/new/rising] [random]** to get a post from hot/new of a subreddit.\n"+
        "**@{displayName} reddit <share link>** or **@{displayName} reddit post <id>** to share a post from reddit and embed it."}

    try:
        secrets = keys.read("reddit-client_id", "reddit-client_secret", "reddit-username", "reddit-password")
        prawInstance = asyncpraw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io",
            client_id=secrets[0], client_secret=secrets[1],
            username=secrets[2], password=secrets[3])
    except Exception as e:
        prawInstance = Exception
        prawException = str(e)

    imageHosts = ["i.redd.it", "i.imgur.com", "media1.giphy.com"]
    videoHosts = ["v.redd.it", "gfycat.com"]

    recentSubmissions = {}

    async def __new__(self, message, command, parentClass):
        if self.prawInstance == Exception:
            await message.channel.send("Reddit is currently unavailable:\n"+self.prawException)
            return
        if "feet" in message.content.lower() or "foot" in message.content.lower() or "spit" in message.content.lower():
            await message.channel.send("```diff\n- I recommend you DON'T unspoiler this! - \n```")
            await message.channel.trigger_typing()

        isSubmission, submissionID = self.submissionID(self, command[2:])
        # If given URL
        if isSubmission:
            try:
                submission = await self.prawInstance.submission(id=submissionID)
                await self.postSubmission(self, message, submission)
            except asyncprawcore.exceptions.NotFound as e:
                await message.channel.send("I can't do that: " + str(e))
        else: # Post from subreddit
            subreddit, sort, index = self.generateArguments(command)
            if not (re.match("^[A-Za-z0-9_]*$", subreddit) and 2 < len(subreddit) <= 21):
                await message.channel.send("That's not a valid subreddit.")
                return
            try: # Get a post
                if subreddit.startswith("u_"):
                    subredditInstance = (await self.prawInstance.redditor(subreddit[2:])).submissions
                else:
                    subredditInstance = await self.prawInstance.subreddit(subreddit)
                if index == "random":
                    try:
                        submission = await subredditInstance.random()
                        submission.id
                    except AttributeError:
                        await message.channel.send("Could not get random post.")
                        index = "first"
                try:
                    channelID = str(message.channel.id)
                except:
                    channelID = str(0)
                if not channelID in self.recentSubmissions:
                    self.recentSubmissions[channelID] = []

                if index != "random":
                    listingGeneratorArgs = {}
                    submission = False
                    if sort == "new":
                        listingGenerator = subredditInstance.new
                    elif sort == "top":
                        listingGenerator = subredditInstance.top
                        listingGeneratorArgs["time_filter"] = "all"
                    elif sort == "rising":
                        listingGenerator = subredditInstance.rising
                    elif sort == "controversial":
                        listingGenerator = subredditInstance.controversial
                        listingGeneratorArgs["time_filter"] = "week"
                    else:
                        listingGenerator = subredditInstance.hot

                    async for submissionIteration in listingGenerator(**listingGeneratorArgs, limit=256):
                        if not submissionIteration.id in self.recentSubmissions[channelID]:
                            if not (submissionIteration.stickied and not ("stickied" in command or "pinned" in command)):
                                submission = submissionIteration
                                break

                    if not submission:
                        await message.channel.send("Could not get a post from that sub.")

                if submission:
                    self.recentSubmissions[channelID] += [submission.id]
                    await self.postSubmission(self, message, submission)
                if len(self.recentSubmissions[channelID]) >= 256:
                    self.recentSubmissions[channelID] = self.recentSubmissions[channelID][32:]
            except asyncprawcore.exceptions.NotFound:
                await message.channel.send("Could not find that subreddit.\nThe subreddit may be private.")
            except asyncprawcore.exceptions.Forbidden as e:
                await message.channel.send("I can't do that: " + str(e) + ".\nThe subreddit may be banned.")
            except asyncprawcore.exceptions.Redirect as e:
                await message.channel.send("I can't do that: " + str(e) + ".\nThe subreddit doesnt exist.")

    def submissionID(self, command):
        if len(command) == 0:
            return False, False
        wordNumber = 0
        if command[0].lower() in ["post", "submission", "id", "#"] and len(command) >= 2:
            wordNumber = 1
        if (command[wordNumber].startswith("https://") or command[wordNumber].startswith("http://") or
                command[wordNumber].startswith("www.reddit.com/") or command[wordNumber].startswith("reddit.com/")):
            if command[wordNumber].startswith("http"):
                id = command[wordNumber].split("/")[6]
            else:
                id = command[wordNumber].split("/")[4]
            if re.match("^[a-z0-9]*$", id) and 10 > len(id) > 5:
                return True, id
            return False, False
        if wordNumber == 1 and 10 > len(command[wordNumber]) > 5:
            if re.match("^[a-z0-9]*$", command[wordNumber]):
                return True, command[wordNumber]
        return False, False

    def generateArguments(command):
        sort = "hot"
        index = None
        if len(command) == 2:
            subreddit = "all"
        else:
            if command[2][:2].lower() == "r/":
                subreddit = command[2][2:]
            else:
                subreddit = command[2]
        if len(command) >= 4:
            if len(command) == 5: options = command[3:5]
            else: options = command[3:4]
            for option in options:
                if option in ["hot", "top", "new", "rising", "controversial"]:
                    sort = option
                elif option == "random":
                    index = option
        if index == None: index = "first"
        return subreddit, sort, index

    async def postSubmission(self, message, submission):
        embed = discord.Embed()
        sendExtra = {}
        # Title stuff
        try:
            submissionInfo = "\nr/" + submission.subreddit.display_name + " - u/" + submission.author.name
        except AttributeError:
            submissionInfo = "\nr/" + submission.subreddit.display_name + " - [DELETED]"
        extras = []
        if submission.over_18: extras += ["NSFW"]
        if submission.spoiler: extras += ["SPOILER"]
        if submission.link_flair_text: extras += ["({0})".format(submission.link_flair_text)]
        if len(extras) >= 1:
            submissionInfo += "\n" + " ".join(extras)

        # If title is too long
        embed.description = ""
        if len(submission.title + submissionInfo) >= 255:
            # Try to remove the last sentence so the title doesnt cut off half way
            shortTitle = submission.title[:(240-len(submissionInfo))].split(".")
            if len(shortTitle) <= 2:
                embed.title = submission.title[:(200-len(submissionInfo))] + "..." + submissionInfo
            else:
                embed.title = ".".join(shortTitle[:-1]) + "..." + submissionInfo
            embed.description += "**" + submission.title + "**\n\n"
        else:
            embed.title = submission.title + submissionInfo


        embed.url = "https://www.reddit.com" + submission.permalink

        # Ratings
        embed.description += "⬆ {0:,}⠀⠀🗨 {1:,}⠀⠀🗓 {2}".format(submission.score, submission.num_comments,
            datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S"))

        # Image & Video
        if submission.domain in self.imageHosts:
            if submission.spoiler or submission.over_18:
                bytesio = io.BytesIO(requests.get(submission.url).content)
                if not bytesio.getbuffer().nbytes >= 8 * 1024 * 1024:
                    filename = "gwen_" + submission.url.split("/")[-1]
                    sendExtra["file"] = discord.File(fp=bytesio, filename=filename, spoiler=(submission.spoiler or submission.over_18))
                    # embed.set_image(url="attachment://" + filename)
                else:
                    sendExtra["content"] = "Could not get the image because it excedes the Discord 8mb limit.\n" + submission.url
            else:
                if submission.url[-5:] == ".gifv":
                    embed.description += "\n\nGifv is not fully supported.\n" + submission.url
                embed.set_image(url=submission.url)
        if submission.domain in self.videoHosts:
            asyncio.sleep(2)
            postJson = requests.get(embed.url+".json", headers={"User-Agent":"Joe#8648 - joeblakeb.github.io"}).json()
            try:
                try:
                    videoFallbackUrl = postJson[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]
                except:
                    videoFallbackUrl = postJson[0]["data"]["children"][0]["data"]["preview"]["reddit_video_preview"]["fallback_url"]
            except:
                videoFallbackUrl = False
                try:
                    sendExtra["content"] = "Could not get video because error " + str(postJson["error"]) + " " + str(postJson["message"])
                except: pass
            if videoFallbackUrl:
                bytesio = io.BytesIO(requests.get(videoFallbackUrl).content)
                if not bytesio.getbuffer().nbytes >= 8 * 1024 * 1024:
                    filename = videoFallbackUrl[9+len(submission.domain):].split(".")[0] + ".mp4"
                    sendExtra["file"] = discord.File(fp=bytesio, filename=filename, spoiler=(submission.spoiler or submission.over_18))
                    embed.set_image(url="attachment://" + filename)
                else:
                    sendExtra["content"] = "Could not get the video because it excedes the Discord 8mb limit.\n" + videoFallbackUrl

        # URL if the post has a link that isn't an image
        if submission.url != embed.url and not submission.domain in self.imageHosts + self.videoHosts:
            embed.description += "\n\n" + submission.url

        # Post description
        description = submission.selftext
        if len(description) + len(embed.description) > 2046:
            description = description[:2008 - len(embed.description)]
            description += "\n(Discord max character limit reached)"
        embed.description += "\n\n" + description


        await message.channel.send(embed=embed, **sendExtra)
