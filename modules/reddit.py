import aiohttp
import asyncpraw, asyncprawcore
import datetime
import discord
import json
import re
import time

import baseClass
from emojis import emojis
import keys

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
        await message.channel.send("TODO: add some help thing here...")

    sortMethods = [{"hot":False, "new":False, "rising":False, "top":True, "controversial":True},
        {"relevant": False, "hot": False, "new":False, "top":True}]
    sortTimes = ["all", "year", "month", "week", "day", "hour"]

    async def subreddit(self, message, commandContent, isSubreddit):
        await message.add_reaction("<:amogus:811622676783169536>")

        subredditName = commandContent.split()[0][2:]
        restOfMessage = commandContent.split()[1:]
        if "search" in restOfMessage[:-1]:
            search = True
            searchTerm = 0
            for word in restOfMessage:
                if searchTerm != 0 and searchTerm != 1: searchTerm += " " + word
                elif searchTerm == 1: searchTerm = word
                elif word == "search": searchTerm = 1
        else:
            search = False
            searchTerm = "N/A"

        sortMethod = list(self.sortMethods[int(search)])[0]
        for word in restOfMessage:
            if word == "search": break
            if word in list(self.sortMethods[int(search)]):
                sortMethod = word
        if self.sortMethods[int(search)][sortMethod]:
            sortTime = "all"
            for word in restOfMessage:
                if word == "search": break
                if word in self.sortTimes:
                    sortTime = word
        else:
            sortTime = "N/A"
        await message.channel.send("isSubreddit: " + str(isSubreddit) + "\nSubreddit: " + subredditName + "\nsortMethod: " + sortMethod + "\nsortTime: " + sortTime + "\nsearch: " + str(search) + "\nsearchTerm: " + searchTerm)

    async def url(self, message, messageContentLower, exclamation):
        try:
            # get id from url
            messageContentLower = messageContentLower[7-(6*int(exclamation)):]
            messageContentLower = messageContentLower.replace("https://", "").replace("http://", "").replace("www.", "")
            if messageContentLower[:8] == "redd.it/":
                submissionID = messageContentLower[8:].split(" ")[0]
            else:
                submissionID = messageContentLower.split("/comments/")[1].split("/")[0]
            # get post from id
            submission = await self.prawInstance.submission(submissionID)
            try:
                await message.edit(suppress=True)
            except: pass
        except asyncprawcore.exceptions.NotFound:
            try:
                for emoji in "⚠️", "4️⃣", "0️⃣", emojis["Four"]:
                    await message.add_reaction(emoji)
                return
            except Exception: pass
        await self.postSubmission(self, message, submission)

    async def postSubmission(self, message, submission, crosspost=False, forceSpoiler=False):
        title = "**" + submission.title + "**"
        try:
            author = "r/" + submission.subreddit.display_name + " • u/" + submission.author.name
        except AttributeError:
            author = "r/" + submission.subreddit.display_name + " • u/[DELETED]"
        spoiler = forceSpoiler
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
                awards += "⠀" + emojis["Coin"] + "{0:,}".format(coinCount)
        stats = emojis["Upvote"]+" {0:,}⠀🗨 {1:,}{2}\n> 🗓 {3}".format(submission.score, submission.num_comments, awards,
            datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M"))

        submissionMetadata = f"> {title}\n> <https://redd.it/{submission.id}>\n> {author}{extras}\n> {stats}"

        if spoiler:
            spoilerLink = "||"
            spoilerText = " ||"
        else:
            spoilerLink = "> "
            spoilerText = ""

        if not hasattr(submission, "post_hint"):
            submission.post_hint = "None"

        if submission.is_self and submission.selftext != "": # Text post
            submissionBody = "\n> \n> " + submission.selftext.replace("\n", "\n> ")
            if hasattr(submission, "poll_data"): # Poll post
                pollLink = "https://www.reddit.com/poll/"+submission.id
                submissionBody = submissionBody.replace(f"\n> \n> [View Poll]({pollLink})", "")
                if submissionBody == "\n> \n> ": submissionBody = ""
                pollData = "\n> "
                open = datetime.datetime.utcnow().timestamp() < submission.poll_data.voting_end_timestamp/1000
                try:
                    options = {}
                    highestCount = 0
                    voteCounts = ""
                    for option in submission.poll_data.options:
                        options[option] = option.vote_count
                        if option.vote_count > highestCount:
                            highestCount = option.vote_count
                    maxVoteLine = (submission.poll_data.total_vote_count*(.5-(len(options)/12))) + (highestCount*(.5+(len(options)/12)))
                    for option in options:
                        voteCounts += f"\n> **{option}**: {options[option]}\n> "
                        voteBlocks = int((options[option] / maxVoteLine) * 240)
                        if options[option] == 1: voteBlocks = 1
                        if options[option] == highestCount: voteBlocks += 2
                        optionVoteLine = "█" * int((voteBlocks-(voteBlocks%8))/8)
                        optionVoteLine += "█▏▎▍▌▋▊▉"[voteBlocks%8]
                        voteCounts += optionVoteLine
                except AttributeError:
                    pollData += "\n> Error getting the option vote counts" + " as the vote has not closed yet"*int(open) + "."
                else:
                    pollData += voteCounts
                pollData += f"\n> Total Votes: {submission.poll_data.total_vote_count}"
                pollData += "\n> " + pollLink + "\n> Voting " + ("closing" * int(open)) + ("closed" * int(not open)) + " at " + time.ctime(submission.poll_data.voting_end_timestamp/1000)
            else: # Regular text post
                pollData = ""

            if spoiler:
                submissionData = spoilerText + submissionBody.replace("|", "¦") + spoilerText
            else:
                submissionData = submissionBody
            if len(submissionMetadata) + len(submissionData) + len(pollData) > 2000:
                submissionData = submissionData[:1956-(len(submissionMetadata)+len(pollData))] + spoilerText + "\n> (Discord max character limit reached)" + pollData
            else:
                submissionData += pollData
        elif submission.url.startswith("https://www.reddit.com/gallery/"): # reddit galleries
            try:
                postJson = await self.postJson(f"https://www.reddit.com{submission.permalink}.json")
                submissionData = ""
                for item in postJson["gallery_data"]["items"]:
                    try: previewURL = postJson["media_metadata"][item["media_id"]]["s"]["u"]
                    except: previewURL = postJson["media_metadata"][item["media_id"]]["s"]["gif"]
                    imageUrl = previewURL.replace("preview.redd.it", "i.redd.it").split("?")[0]
                    submissionData += f"\n{spoilerLink}{imageUrl}{spoilerText}"
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
                    submissionData = submissionData.split("?source=fallback")[0]
                submissionData = f"\n{spoilerLink}{submissionData}{spoilerText}"
            except Exception as e:
                e = e.replace("\n", "\n> ")
                submissionData = f"\n> {e}\n{spoilerLink}{submission.url}{spoilerText}"
        elif submission.url == "https://www.reddit.com" + submission.permalink: # Nothing, should never be used
            submissionData = ""
        elif re.match("https:\/\/www.reddit.com\/r\/[^\s\/]+\/comments\/[^\s\/]+/", submission.url) and not crosspost: # Crossposts
            try:
                submissionID = submission.url.split("/comments/")[1].split("/")[0]
                submission = await self.prawInstance.submission(submissionID)
                crosspostData = await self.postSubmission(self, message, submission, crosspost=True, forceSpoiler=spoiler)
                crosspostLink = f"\n> \n> Crosspost: <https://redd.it/{submissionID}>\n"
                if len(submissionMetadata) + len(crosspostData) + len(crosspostLink) > 2000:
                    submissionData = crosspostLink + crosspostData[:1956-(len(submissionMetadata)+len(crosspostLink))] + spoilerText + "\n> (Discord max character limit reached)"
                else:
                    submissionData = crosspostLink + crosspostData
            except asyncprawcore.exceptions.NotFound:
                submissionData = f"\n> \n> HTTP error 404 while getting crosspost.\n{spoilerLink}{submission.url}{spoilerText}"
        else: # Other links
            submissionData = f"\n{spoilerLink}{submission.url}{spoilerText}"

        if crosspost:
            return submissionMetadata + submissionData
        else:
            await message.channel.send(submissionMetadata + submissionData)
            print(str(message.author)+" NSFW:" + str(submission.over_18) +" "+ submission.subreddit.display_name+" "+ submission.id, flush=True)

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

# Use old post finder code till i have actually done the new one
# legacyReddit.py (not commited) is reddit.py from before the rewrite
# with only the prawInstance code removed
import bz2
import os
import json
from legacyReddit import reddit as oldReddit
class legacyReddit(oldReddit):
    postSubmission = reddit.postSubmission
    postJson = reddit.postJson
    prawInstance = reddit.prawInstance
    async def subreddit(self, message, commandContent):
        message.content = "joebot reddit " + commandContent[1:]
        command = message.content.split(" ")
        await self.__new__(self, message, command, None)

    async def user(self, message, commandContent):
        message.content = "joebot reddit r/u_" + commandContent[3:]
        print(message.content)
        command = message.content.split(" ")
        await self.__new__(self, message, command, None)

reddit.mentionedCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":True}]
reddit.mentionedCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":False}]
reddit.mentionedCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":False}]
reddit.exclamationCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":True}]
reddit.exclamationCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":False}]
reddit.exclamationCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":True}]
reddit.closeTasks += [reddit.prawInstance.close()]




reddit.mentionedCommands["!r\/([^\s\/]+)(?!\S)"] = [legacyReddit.subreddit, ["message", "commandContent"], {"self":legacyReddit}]
reddit.mentionedCommands["!u\/[A-Za-z0-9_-]+(?!\S)"] = [legacyReddit.user, ["message", "commandContent"], {"self":legacyReddit}]
reddit.exclamationCommands["!r\/([^\s\/]+)(?!\S)"] = [legacyReddit.subreddit, ["message", "commandContent"], {"self":legacyReddit}]
reddit.exclamationCommands["!u\/[A-Za-z0-9_-]+(?!\S)"] = [legacyReddit.user, ["message", "commandContent"], {"self":legacyReddit}]
reddit.startTasks += [legacyReddit.loadRecentSubmissions(legacyReddit)]
reddit.closeTasks += [legacyReddit.saveRecentSubmissions(legacyReddit)]
