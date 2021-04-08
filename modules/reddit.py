import aiohttp
import asyncpraw, asyncprawcore
import datetime
import discord
import json
import time

import baseClass
from emojis import emojis
import keys

# TODO:
# reddit: re route to subreddit, user, or url, fallback to r/all if none
# subreddit
# user
# url: get id from url
# postSubmission: support videos and galleries

class reddit(baseClass.baseClass):
    try:
        secrets = keys.read("reddit-client_id", "reddit-client_secret", "reddit-username", "reddit-password")
        prawInstance = asyncpraw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io",
            client_id=secrets[0], client_secret=secrets[1],
            username=secrets[2], password=secrets[3])
    except Exception as e:
        prawInstance = Exception
        prawException = str(e)

    recentPosts = {}
    # {"ChannelID":{"DayOfYear":[PostIDs]}}
    subredditCache = {}
    # {"Subreddit":[0=Timestamp, 1:=PostIDs]}
    cursedSubreddits = {}
    # {"Subreddit":{"BanTime":Seconds, "NSFWOnlyBan":Bool "ContentWarning":"text", "BlockContent":("None"|NoMedia"|"Blocked Reason Text"|[ListOfImageURLs, #seperated])}}
    # cursedSubreddits.txt: [subredditname], Ban[BanTime](NSFW| ), [BlockContent], CW:[ContentWarning, use \n](must be at end of line)
    bannedUsers = {}
    # {"UserID|ServerID":["BannedUntilTimestamp", NSFW:True]}

    async def reddit(self, message):
        return await message.add_reaction("❌")

    async def subreddit(self, message):
        print(time.time())
        subredditInstance = await self.prawInstance.subreddit("196")
        print(time.time())
        postIDs = []
        async for post in subredditInstance.hot(limit=16):
            postIDs += [post.id]
        print(postIDs)
        print(time.time())
        return await message.add_reaction("❌")

    async def user(self, message):
        return await message.add_reaction("❌")

    async def url(self, message, messageContentLower, exclamation):
        try:
            # get id from url
            messageContentLower = messageContentLower[7-(6*int(exclamation)):]
            messageContentLower = messageContentLower.replace("https://", "").replace("http://", "").replace("www.", "")
            if messageContentLower[:8] == "redd.it/":
                submissionID = messageContentLower[8:]
            else:
                submissionID = messageContentLower.split("/comments/")[1].split("/")[0]
            # get post from id
            submission = await self.prawInstance.submission(submissionID)

            await message.edit(suppress=True)
        except asyncprawcore.exceptions.NotFound:
            try:
                for emoji in "⚠️", "4️⃣", "0️⃣", emojis["Four"]:
                    await message.add_reaction(emoji)
                return
            except Exception: pass
        await self.postSubmission(self, message, submission)

    async def postSubmission(self, message, submission):
        title = "**" + submission.title + "**"
        try:
            author = "r/" + submission.subreddit.display_name + " • u/" + submission.author.name
        except AttributeError:
            author = "r/" + submission.subreddit.display_name + " • u/[DELETED]"
        spoiler = False
        extras = []
        if submission.spoiler:
            extras += ["**SPOILER**"]
            spoiler = True
            title = "⚠️ " + title
        if submission.over_18:
            extras += ["**NSFW**"]
            spoiler = True
            title = "🔞 " + title
        if submission.link_flair_text:
            extras += ["({0})".format(submission.link_flair_text)]
        extras = " ".join(extras)
        if extras != "":
            extras = "\n> " + extras

        awards = ""
        awardCount = 0
        coinCount = 0
        for award in submission.all_awardings:
            awardCount += award["count"]
            coinCount += award["count"] * award["coin_price"]
        if awardCount != 0:
            awards = "⠀" + emojis["RedditGold"] + "{0:,}".format(awardCount)
            if "--coin" in message.content.lower():
                awards += "⠀" + emojis["Coin"] + "⠀{0:,}".format(coinCount)
        stats = emojis["Upvote"]+" {0:,}⠀🗨 {1:,}{2}\n> 🗓 {3}".format(submission.score, submission.num_comments, awards,
            datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M"))

        submissionMetadata = f"> {title}\n> <https://redd.it/{submission.id}>\n> {author}{extras}\n> {stats}"

        if spoiler:
            spoilerLink = "||"
            spoilerText = "||"
            if "?" in submission.url:
                queryExtra = "&?"
            else:
                queryExtra = "?"
        else:
            spoilerLink = "> "
            spoilerText = ""
            queryExtra = ""

        if submission.is_self and submission.selftext != "": # Text post
            print(submission.selftext)
            if spoiler:
                submissionData = "\n> " + spoilerText + submission.selftext.replace("\n", "\n> ").replace("|", "¦") + spoilerText
            else:
                submissionData = "\n> " + submission.selftext.replace("\n", "\n> ")
            if len(submissionMetadata) + len(submissionData) > 2000:
                submissionData = submissionData[:1956-len(submissionMetadata)] + spoilerText + "\n> (Discord max character limit reached)"
        elif submission.url.startswith("https://www.reddit.com/gallery/"): # reddit galleries
            try:
                postJson = await self.postJson(f"https://www.reddit.com{submission.permalink}.json")
                submissionData = ""
                for item in postJson["gallery_data"]["items"]:
                    try: previewURL = postJson["media_metadata"][item["media_id"]]["s"]["u"]
                    except: previewURL = postJson["media_metadata"][item["media_id"]]["s"]["gif"]
                    imageUrl = previewURL.replace("preview.redd.it", "i.redd.it").split("?")[0]
                    submissionData += f"\n{spoilerLink}{imageUrl}{queryExtra}{spoilerText}"
            except Exception as e:
                e = e.replace("\n", "\n> ")
                submissionData = f"\n> {e}"
        elif submission.post_hint == "hosted:video": # Video post (not stuff like youtube)
            try:
                postJson = await self.postJson(f"https://www.reddit.com{submission.permalink}.json")
                try:
                    submissionData = postJson["secure_media"]["reddit_video"]["fallback_url"]
                except:
                    submissionData = postJson["preview"]["reddit_video_preview"]["fallback_url"]
                if "?" in submissionData and spoiler: submissionData += "&?"
                elif spoiler: submissionData += "?"
                else:
                    queryExtra = ""
                    submissionData = submissionData.split("?source=fallback")[0]
                submissionData = f"\n{spoilerLink}{submissionData}{spoilerText}"
            except Exception as e:
                e = e.replace("\n", "\n> ")
                submissionData = f"\n> {e}\n{spoilerLink}{submission.url}{queryExtra}{spoilerText}"
        else: # Other links
            if submission.url != "https://www.reddit.com" + submission.permalink:
                submissionData = f"\n{spoilerLink}{submission.url}{queryExtra}{spoilerText}"
            else:
                submissionData = ""

        await message.channel.send(submissionMetadata + submissionData)
        print(str(message.author)+" NSFW:" + str(submission.over_18) +" "+ submission.subreddit.display_name+" "+ submission.id)

    async def postJson(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception("\n> HTTP error getting fallback URL: " + str(resp.status))
                response = await resp.text()
                postJson = json.loads(response)
                # Get post data, crosspost data if it exists.
                try: return postJson[0]["data"]["children"][0]["data"]["crosspost_parent_list"][0]
                except: return postJson[0]["data"]["children"][0]["data"]

reddit.mentionedCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.user, ["message"], {"self":reddit}]
reddit.mentionedCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":False}]
reddit.exclamationCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.user, ["message"], {"self":reddit}]
reddit.exclamationCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":True}]
reddit.closeTasks += [reddit.prawInstance.close()]
