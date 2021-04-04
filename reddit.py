import discord
import asyncpraw, asyncprawcore
import requests
import io
import re
import asyncio
import datetime
import os
import json
import bz2
import time
import sys
import random

import keys

class redditv2:

    try:
        secrets = keys.read("reddit-client_id", "reddit-client_secret", "reddit-username", "reddit-password")
        prawInstance = asyncpraw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io",
            client_id=secrets[0], client_secret=secrets[1],
            username=secrets[2], password=secrets[3])
    except Exception as e:
        prawInstance = Exception
        prawException = str(e)

    recentSubmissions = {}

    async def loadRecentSubmissions(self):
        try:
            with bz2.open("tmp/recentSubmissions.txt.bz2", "rb") as recentSubmissionsFile:
                self.recentSubmissions = json.loads(str(recentSubmissionsFile.read(), "utf-8"))
        except FileNotFoundError: pass

    async def saveRecentSubmissions(self):
        os.makedirs("tmp", exist_ok=True)
        with bz2.open("tmp/recentSubmissions.txt.bz2", "wb") as recentSubmissionsFile:
            recentSubmissionsFile.write(bytes(json.dumps(self.recentSubmissions, indent=4), "utf-8"))

    async def __new__(self, message, command, parentClass):
        await message.channel.send("Reddit V2 is currently unavailable")


class reddit(redditv2):
    help = {"list": True, "ListPriority": 5, "Title":"Reddit",
        "ShortHelp": "Get a post from a subreddit.",
        "LongHelp": "Get a post from a subreddit.\n"+
        "**@{displayName} reddit** to get a post from the front page.\n"+
        "**@{displayName} reddit r/<subreddit>** or **@{displayName} r/<subreddit>** "+
        "to get a post from the front page of that subreddit.\n"+
        "**@{displayName} reddit r/<subreddit> [hot/top/new/rising] [random]** to get a post from hot/new of a subreddit.\n"+
        "**@{displayName} reddit <share link>** or **@{displayName} reddit post <id>** to share a post from reddit and embed it."}

    dashResolutions = ["1080", "720", "480", "360", "240", "96"]

    typing = False

    async def __new__(self, message, command, parentClass):
        for role in message.author.roles:
            if str(role).lower() == "no joebot":
                return await message.add_reaction("⛔")

        await message.channel.trigger_typing()

        if self.prawInstance == Exception:
            await message.channel.send("Reddit is currently unavailable:\n"+self.prawException)
            return

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
                timeStart = time.time()
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

                    async for submissionIteration in listingGenerator(**listingGeneratorArgs, limit=512):
                        if not submissionIteration.id in self.recentSubmissions[channelID]:
                            if not (submissionIteration.stickied and not ("stickied" in command or "pinned" in command)):
                                submission = submissionIteration
                                break

                    if not submission:
                        await message.channel.send("Could not get a post from that sub.")

                    now = datetime.datetime.now()
                    timeNow = int(str(now.hour)+("0"+str(now.minute))[-2:])
                    if (submission.over_18 and (now.weekday() in [2,4])) and (timeNow >= 900 and timeNow <= 1600) and message.author.id == 217412254608392193:
                        return await message.add_reaction("⛔")
                    if submission.over_18:
                        for role in message.author.roles:
                            if str(role).lower() == "no nsfw":
                                return await message.add_reaction("⛔")
                        # if submission.subreddit.display_name.lower() in ["eyeblech"]:
                        #     return await message.add_reaction("❌")

                #print("Chose post", time.time() - timeStart)
                if submission:
                    self.recentSubmissions[channelID] += [submission.id]
                    await self.postSubmission(self, message, submission)
                if len(self.recentSubmissions[channelID]) >= 512:
                    self.recentSubmissions[channelID] = self.recentSubmissions[channelID][32:]
            except asyncprawcore.exceptions.NotFound:
                await message.channel.send("Could not find that subreddit.\nThe subreddit may be private.")
            except asyncprawcore.exceptions.Forbidden as e:
                await message.channel.send("I can't do that: " + str(e) + ".\nThe subreddit may be banned.")
            except asyncprawcore.exceptions.Redirect as e:
                await message.channel.send("I can't do that: " + str(e) + ".\nThe subreddit doesnt exist.")
            except Exception as e:
                await message.channel.send("I can't do that: " + str(e))

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
        timeStart = time.time()
        embed = discord.Embed()
        sendExtra = {}
        sendExtra2 = {}
        addUrlToDescription = True
        # Title stuff
        await submission.subreddit.load()
        if submission.subreddit.community_icon == "": submission.subreddit.community_icon =  submission.subreddit.icon_img
        try:
            embed.set_author(name="r/" + submission.subreddit.display_name + " • u/" + submission.author.name, icon_url=submission.subreddit.community_icon)
        except AttributeError:
            embed.set_author(name="r/" + submission.subreddit.display_name + " • [DELETED]", icon_url=submission.subreddit.community_icon)
        try:
            embed.color = int(submission.subreddit.primary_color[1:], 16)
        except: pass
        extras = []
        submissionInfo = ""
        if submission.over_18: extras += ["NSFW"]
        if submission.spoiler: extras += ["SPOILER"]
        if submission.link_flair_text: extras += ["({0})".format(submission.link_flair_text)]
        if len(extras) >= 1:
            submissionInfo = "\n" + " ".join(extras)

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
        #print("Embed Meta", time.time() - timeStart)
        timeStart = time.time()

        # Ratings
        embed.description += "⬆ {0:,}⠀⠀🗨 {1:,}⠀⠀🗓 {2}".format(submission.score, submission.num_comments,
            datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M"))

        # If post is text set post hint
        await submission.load()

        try: submission.post_hint
        except Exception as e:
            try: submission.post_hint
            except: submission.post_hint = "none"

        if (submission.over_18 and datetime.datetime.today().strftime("%m%d") == "0401") or (submission.subreddit.display_name.lower() in ["eyeblech"]):
            submission.url = random.choice(["https://cdn.discordapp.com/attachments/796434329831604288/827110312183857152/HoodCate.png",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110903920066601/DontMessWithHoodCate.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110907443544064/HoodCate2.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110909154951188/HoodCateAd.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110909733502986/HoodCateChill.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110911927255050/HoodCateHD.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110919783317504/HoodCateSleep2.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110921268756491/HoodCateSmug.png",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110913080950804/HoodCateLeft.png",
                "https://cdn.discordapp.com/attachments/796434329831604288/827110914712272896/HoodCateRight.png",
                "https://cdn.discordapp.com/attachments/796434329831604288/827111935282774016/YoungHoodCate2.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827111933664690196/YoungHoodCate.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827111931416150076/HoodCateSleep3.jpg",
                "https://cdn.discordapp.com/attachments/796434329831604288/827111931419820053/HoodCateSleep.png"])
            submission.post_hint = "image"
            submission.domain = "i.redd.it"

        # Image & Video
        if submission.post_hint == "image" or submission.domain == "i.redd.it":
            addUrlToDescription = False
            try:
                await self.embedImage(submission, embed, sendExtra, submission.url)
            except PermissionError:
                submission.post_hint = "gifTooLarge"
            await message.channel.trigger_typing()
        if submission.url.startswith("https://www.reddit.com/gallery/"):
            await asyncio.sleep(1)
            await message.channel.trigger_typing()
            postJson = await self.postJson(embed.url)

            mediaID = postJson["gallery_data"]["items"][0]["media_id"]
            try:
                previewURL = postJson["media_metadata"][mediaID]["s"]["u"]
            except:
                try:
                    previewURL = postJson["media_metadata"][mediaID]["s"]["gif"]
                except:
                    previewURL = False
            if previewURL:
                imageURL = previewURL.replace("preview.redd.it", "i.redd.it").split("?")[0]
                try:
                    await self.embedImage(submission, embed, sendExtra, imageURL)
                except PermissionError:
                    submission.post_hint = "gifTooLarge"
                await message.channel.trigger_typing()
            else:
                embed.description += "\n\nCould not get gallery preview."
            addUrlToDescription = False
            embed.description += "\n\nFull gallery with " + str(len(postJson["gallery_data"]["items"])) + " images:\n" + submission.url
        if submission.post_hint in ["hosted:video", "rich:video", "gifTooLarge"] or submission.domain == "v.redd.it" or (
                submission.url[-4:] in ["gifv", ".gif"] and submission.post_hint != "image"):
            await asyncio.sleep(.5)
            postJson = await self.postJson(embed.url)
            # Get fallback url
            try:
                try:
                    videoFallbackUrl = postJson["secure_media"]["reddit_video"]["fallback_url"]
                except:
                    videoFallbackUrl = postJson["preview"]["reddit_video_preview"]["fallback_url"]
            except:
                videoFallbackUrl = False

            # Get video
            if videoFallbackUrl:
                await message.channel.trigger_typing()
                if videoFallbackUrl.endswith("?source=fallback"):
                    videoFallbackUrl = videoFallbackUrl[:-16]

                if videoFallbackUrl.split("/")[-1].startswith("DASH_"):
                    if videoFallbackUrl.split("/")[-1].endswith(".mp4"):
                        fallbackResolution = videoFallbackUrl.split("/")[-1][5:-4]
                    else:
                        fallbackResolution = videoFallbackUrl.split("/")[-1][5:]
                    try:
                        dashResolutions = self.dashResolutions[self.dashResolutions.index(fallbackResolution):]

                    except:
                        dashResolutions = [fallbackResolution] + self.dashResolutions

                    fallbackUrls = []
                    for dashResolution in dashResolutions:
                        if videoFallbackUrl.split("/")[-1].endswith(".mp4"):
                            fallbackUrls += ["DASH_" + dashResolution + ".mp4"]
                        else:
                            fallbackUrls += ["DASH_" + dashResolution]

                    fallbackUrlMain = videoFallbackUrl[:-len(fallbackUrls[0])]
                else:
                    fallbackUrls = [videoFallbackUrl.split("/")[-1]]

                bytesio, fallbackUrl = await self.getFile(message, embed, fallbackUrlMain, fallbackUrls)

                if bytesio:
                    filename = submission.id + "_" + fallbackUrl.lower().split("?")[0]
                    if not videoFallbackUrl.split("/")[-1].endswith(".mp4"): filename += ".mp4"
                    sendExtra["file"] = discord.File(fp=bytesio, filename=filename, spoiler=(submission.spoiler or submission.over_18))
                else:
                    if submission.spoiler or submission.over_18: sendExtra2["content"] = "||" + videoFallbackUrl + "||"
                    else: sendExtra2["content"] = videoFallbackUrl
                addUrlToDescription = False
            else:
                if submission.url.endswith("gif"):
                    embed.description += "\n\nCould not embed the gif because it is over 8MB and has no fallback video.\n" + submission.url
                    addUrlToDescription = False
                else:
                    addUrlToDescription = False
                    if submission.spoiler or submission.over_18: sendExtra2["content"] = "||" + submission.url + "||"
                    else: sendExtra2["content"] = submission.url


        #print("Embed Media", time.time() - timeStart)
        timeStart = time.time()

        # URL if the post has a link that isn't an image
        if submission.url != embed.url and addUrlToDescription:
            embed.description += "\n\n" + submission.url

        # Post description
        description = submission.selftext
        if len(description) + len(embed.description) > 2046:
            description = description[:2008 - len(embed.description)]
            description += "\n(Discord max character limit reached)"
        embed.description += "\n\n" + description

        #if submission.over_18:
        #    sendExtra["content"] = "Here you go " + message.author.display_name
        print(str(message.author)+" NSFW:" + str(submission.over_18) +" "+ submission.subreddit.display_name+" "+ submission.id)
        sys.stdout.flush()
        await message.channel.send(embed=embed, **sendExtra)
        if sendExtra2 != {}:
            await message.channel.send(**sendExtra2)

        #print("Send", time.time() - timeStart)

    async def embedImage(submission, embed, sendExtra, url):
        loop = asyncio.get_event_loop()
        if submission.spoiler or submission.over_18 or submission.domain != "i.redd.it":
            get = await loop.run_in_executor(None, requests.get, url)
            bytesio = io.BytesIO(get.content)
            if not bytesio.getbuffer().nbytes >= 8 * 1024 * 1024:
                filename = "gwen_" + url.split("/")[-1].split("?")[0]
                sendExtra["file"] = discord.File(fp=bytesio, filename=filename, spoiler=(submission.spoiler or submission.over_18))
                embed.set_image(url="attachment://" + filename)
            else:
                if url[-4:] == ".gif" or url[-4:] == ".gifv":
                    raise PermissionError
                else:
                    embed.description += "\n\nCould not get the image because it excedes the Discord 8MB limit.\n" + url
        else:
            embed.set_image(url=url)

    async def postJson(url):
        loop = asyncio.get_event_loop()
        get = await loop.run_in_executor(None, reddit.get, url+".json")
        postJson = get.json()
        # If crosspost
        try:
            postJson = postJson[0]["data"]["children"][0]["data"]["crosspost_parent_list"][0]
        # If not
        except:
            postJson = postJson[0]["data"]["children"][0]["data"]
        return postJson

    async def getFile(message, embed, urlMain, subUrls):
        loop = asyncio.get_event_loop()
        bestQuality = [0, ""]
        for subUrl in subUrls:
            await message.channel.trigger_typing()
            head = await loop.run_in_executor(None, requests.head, urlMain + subUrl)
            fileSize = int(head.headers["Content-Length"])
            if fileSize >= 8 * 1024 ** 2 or head.status_code != 200:
                if fileSize > bestQuality[0]:
                    bestQuality = [fileSize, subUrl]
                bytesio = False
            else:
                get = await loop.run_in_executor(None, requests.get, urlMain + subUrl)
                bytesio = io.BytesIO(get.content)
                if bytesio.getbuffer().nbytes >= 8 * 1024 ** 2 or get.status_code != 200:
                    bytesio = False
                else:
                    break
        if bestQuality[0] != 0:
            fileSize = int(bestQuality[0]/(1024**2))
            if fileSize == 8: fileSize = 9
            embed.description += "\n\n[Higher quality ({0}MB)]({1})".format(fileSize, urlMain + bestQuality[1])
        return bytesio, subUrl

    def get(url): return requests.get(url+".json", headers={"User-Agent":"Joe#8648 - joeblakeb.github.io"})
