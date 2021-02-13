import discord
import asyncpraw, asyncprawcore
import requests
import io
import re

import keys

import warnings
warnings.filterwarnings('ignore')

# embed = discord.Embed()
# embed.title = subreddit
# bytesio = io.BytesIO(requests.get(subreddit).content)
# file = discord.File(fp=bytesio, filename="nigga.png", spoiler=("spoiler" in command))
# embed.set_image(url="attachment://nigga.png")
# embed.set_image(url="https://cdn.discordapp.com/attachments/643102110375870483/809892611442999317/HT1HhQW8.jpg")
#
# await message.channel.send("Subreddit: " + subreddit, embed=embed, file=file)

class reddit:
    help = {"list": True, "ListPriority": 5, "Title":"Reddit",
        "ShortHelp": "Get a post from a subreddit. **Currently work in progress.**",
        "LongHelp": "Get a post from a subreddit.\n"+
        "\n✅ make something to store the store the keys so I dont accidentally upload the api keys to github\n"+
        "✅ work out what the user wants the bot to do\n"+
        "❌ get post from hot of subreddit\n"+
        "❌ get post from top/new of subreddit\n"+
        "❌ get random post\n"+
        "❌ get certain post / most recent / top of all time\n"+
        "✅ embed the content\n"+
        "✅ post from reddit share link\n"+
        "❌ bugfixes\n"+
        "\nFuture commands:\n"+
        "**@{displayName} reddit** to get a post from the front page.\n"+
        "**@{displayName} reddit r/<subreddit>** or **@{displayName} r/<subreddit>** "+
        "to get a post from the front page of that subreddit.\n"+
        "**@{displayName} reddit r/<subreddit> [top/new] [<number>/random]** to get a post from hot/new of a subreddit.\n"+
        "**@{displayName} reddit <share link>** or **@{displayName} reddit post <id>** to share a post from reddit and embed it."}

    async def __new__(self, message, command, parentClass):
        await dev(message, command, parentClass)
        for word in ["feet", "foot", "hentai", "rule34", "loli", "porn"]:
            if word in message.content:
                await message.channel.send("Fuck off degenerate.")
                return
        await message.channel.send("See **joebot help reddit** to see progress on the reddit command.")

class dev:
    try:
        secrets = keys.read("reddit-client_id", "reddit-client_secret", "reddit-username", "reddit-password")
        prawInstance = asyncpraw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io",
            client_id=secrets[0], client_secret=secrets[1],
            username=secrets[2], password=secrets[3])
    except Exception as e:
        prawInstance = Exception
        prawException = str(e)

    async def __new__(self, message, command, parentClass):
        if self.prawInstance == Exception:
            await message.channel.send("Reddit is currently unavailable:\n"+self.prawException)
            return

        isSubmission, submissionID = self.submissionID(self, command[2:])
        if isSubmission:
            try:
                submission = await self.prawInstance.submission(id=submissionID)
                await self.postSubmission(message, submission)
            except asyncprawcore.exceptions.NotFound as e:
                await message.channel.send("I can't do that: " + str(e))
        else:
            subreddit, sort, index = self.generateArguments(command)
            if re.match("^[A-Za-z0-9_]*$", subreddit) and 2 < len(subreddit) <= 21:
                await message.channel.send("Subreddit: " + subreddit + " Sort: " + sort + " Index: " + str(index))
            else:
                await message.channel.send("That's not a valid subreddit.")

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
                if option in ["hot", "top", "new"]:
                    sort = option
                elif option == "random":
                    index = option
                else:
                    try: index = int(option)
                    except: pass
        if index == None and sort == "hot": index = "random"
        elif index == None: index = 1
        return subreddit, sort, index

    async def postSubmission(message, submission):
        embed = discord.Embed()
        includeFile = False
        # Title stuff
        embed.title = submission.title + "\nr/" + submission.subreddit.display_name + " - u/" + submission.author.name
        extras = []
        if submission.over_18: extras += ["NSFW"]
        if submission.spoiler: extras += ["SPOILER"]
        if submission.link_flair_text: extras += ["({0})".format(submission.link_flair_text)]
        if len(extras) >= 1:
            embed.title += "\n" + " ".join(extras)
        embed.url = "https://www.reddit.com" + submission.permalink

        # Ratings
        embed.description = "⬆ {0}⠀⠀🗨 {1}".format(submission.score, submission.num_comments)

        # Image
        if submission.domain == 'i.redd.it':
            if submission.spoiler or submission.over_18:
                bytesio = io.BytesIO(requests.get(submission.url).content)
                file = discord.File(fp=bytesio, filename="gwen_" + submission.url.split("/")[-1], spoiler=True)
                embed.set_image(url="attachment://gwen_" + submission.url.split("/")[-1])
                includeFile = True
            else:
                embed.set_image(url=submission.url)

        # URL if the post has a link that isn't an image
        if submission.url != embed.url and not submission.domain == 'i.redd.it':
            embed.description += "\n\n" + submission.url

        # Post description
        description = submission.selftext
        if len(description) + len(embed.description) > 2046:
            description = description[:2008 - len(embed.description)]
            description += "\n(Discord max character limit reached)"
        embed.description += "\n\n" + description

        if includeFile:
            await message.channel.send(embed=embed, file=file)
        else:
            await message.channel.send(embed=embed)
