import aiohttp
import datetime
import discord
import json
import re
import time
import urllib.parse

import baseClass
from emojis import emojis
import keys

class reddit(baseClass.baseClass):
    tempRecentPostsList = []
    recentPosts = {}
    # {"ChannelID":{"DayOfYear":[PostIDs]}}
    subredditCache = {}
    # {"Subreddit":[0=Timestamp, 1:=PostIDs]}

    async def reddit(self, message):
        await message.channel.send("TODO: add some help thing here...")

    sortMethods = [{"hot":False, "new":False, "rising":False, "top":True, "controversial":True},
        {"relevant": False, "hot": False, "new":False, "top":True}]
    sortTimes = ["all", "year", "month", "week", "day", "hour"]

    async def subreddit(self, message, commandContent, isSubreddit):
        # Get what user wants from message
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

        sortMethod = list(self.sortMethods[int(search)])[0]
        for word in restOfMessage:
            if word == "search": break
            if word in list(self.sortMethods[int(search)]):
                sortMethod = word
        sortTime = "all"
        for word in restOfMessage:
            if word == "search": break
            if word in self.sortTimes:
                sortTime = word
        else:
            sortTime = None

        # Convert that to a URL
        url = f"https://www.reddit.com/{('user'*int(not isSubreddit))+('r'*int(isSubreddit))}/{subredditName}/"
        if search:
            url += f"search.json?q={urllib.parse.quote(searchTerm, safe='')}&restrict_sr=1&sort={sortMethod}&t={sortTime}{'&include_over_18=on'*int(message.channel.is_nsfw())}"
        else:
            url += f"{sortMethod}.json?t={sortTime}{'&include_over_18=on'*int(message.channel.is_nsfw())}"

        # Get the search from the URL
        posts = await self.getResponseJson(self, url)

        # Select post to send to channel
        for post in posts:
            if not post["data"]["id"] in self.tempRecentPostsList and not (post["data"]["stickied"] and not (
                    "pinned" in message.content.lower() or "stickied" in message.content.lower())):
                self.tempRecentPostsList.append(post["data"]["id"])
                return await self.postSubmission(self, message, post["data"])
        await message.add_reaction("<:amogus:811622676783169536>")

    async def getResponseJson(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(str(resp.status))
                response = await resp.text()
        responseJson = json.loads(response)
        return responseJson["data"]["children"]

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
            submissionJson = await self.postJson(submissionID)
            try:
                await message.edit(suppress=True)
            except: pass
        except Exception as e:
            await message.add_reaction("⚠️")
            try:
                if e == "404":
                    for emoji in "4️⃣", "0️⃣", emojis["Four"]:
                        await message.add_reaction(emoji)
            except Exception: pass
        await self.postSubmission(self, message, submissionJson)

    async def postSubmission(self, message, submissionJson, crosspost=False, forceSpoiler=False):
        title = "**" + submissionJson["title"] + "**"
        author = submissionJson["subreddit_name_prefixed"] + " • u/" + submissionJson["author"]
        spoiler = forceSpoiler
        extras = []
        if submissionJson["stickied"]:
            extras += ["**PINNED BY MODERATORS**"]
            title = "📌 " + title
        if submissionJson["spoiler"]:
            extras += ["**SPOILER**"]
            spoiler = True
            title = "⚠️ " + title
        if submissionJson["over_18"]:
            extras += ["**NSFW**"]
            spoiler = True
            title = "🔞 " + title
        if submissionJson["link_flair_text"]:
            extras += ["({0})".format(submissionJson["link_flair_text"])]
        extras = " ".join(extras)
        if extras != "":
            extras = "\n> " + extras

        awards = ""
        awardCount = 0
        coinCount = 0
        for award in submissionJson["all_awardings"]:
            awardCount += award["count"]
            coinCount += award["count"] * award["coin_price"]
        if awardCount != 0:
            awards = "⠀" + emojis["RedditGold"] + "{0:,}".format(awardCount)
            if "--coin" in message.content.lower():
                awards += "⠀" + emojis["Coin"] + "{0:,}".format(coinCount)
        stats = emojis["Upvote"]+" {0:,}⠀🗨 {1:,}{2}\n> 🗓 {3}".format(submissionJson["score"], submissionJson["num_comments"], awards,
            datetime.datetime.fromtimestamp(submissionJson["created_utc"]).strftime("%Y-%m-%d %H:%M"))

        submissionMetadata = f"> {title}\n> <https://redd.it/{submissionJson['id']}>\n> {author}{extras}\n> {stats}"

        if spoiler:
            spoilerLink = "||"
            spoilerText = " ||"
        else:
            spoilerLink = "> "
            spoilerText = ""

        try:
            postHint = submissionJson["post_hint"]
        except:
            postHint = "None"

        if submissionJson["is_self"] and submissionJson["selftext"] != "": # Text post
            submissionBody = "\n> \n> " + submissionJson["selftext"].replace("\n", "\n> ")
            try:
                pollLink = "https://www.reddit.com/poll/"+submissionJson["id"]
                submissionBody = submissionBody.replace(f"\n> \n> [View Poll]({pollLink})", "")
                if submissionBody == "\n> \n> ": submissionBody = ""
                pollData = "\n> "
                open = datetime.datetime.utcnow().timestamp() < submissionJson["poll_data"]["voting_end_timestamp"]/1000
                try:
                    options = {}
                    highestCount = 0
                    voteCounts = ""
                    for option in submissionJson["poll_data"]["options"]:
                        options[option["text"]] = option["vote_count"]
                        if option["vote_count"] > highestCount:
                            highestCount = option["vote_count"]
                    maxVoteLine = (submissionJson["poll_data"]["total_vote_count"]*(.5-(len(options)/12))) + (highestCount*(.5+(len(options)/12)))
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
                pollData += f"\n> Total Votes: {submissionJson['poll_data']['total_vote_count']}"
                pollData += "\n> " + pollLink + "\n> Voting " + ("closing" * int(open)) + ("closed" * int(not open)) + " at " + time.ctime(submissionJson["poll_data"]["voting_end_timestamp"]/1000)
            except:
                pollData = ""

            if spoiler:
                submissionData = spoilerText + submissionBody.replace("|", "¦") + spoilerText
            else:
                submissionData = submissionBody
            if len(submissionMetadata) + len(submissionData) + len(pollData) > 2000:
                submissionData = submissionData[:1956-(len(submissionMetadata)+len(pollData))] + spoilerText + "\n> (Discord max character limit reached)" + pollData
            else:
                submissionData += pollData
        elif submissionJson["url"].startswith("https://www.reddit.com/gallery/"): # reddit galleries
            try:
                submissionData = ""
                for item in submissionJson["gallery_data"]["items"]:
                    try: previewURL = submissionJson["media_metadata"][item["media_id"]]["s"]["u"]
                    except: previewURL = submissionJson["media_metadata"][item["media_id"]]["s"]["gif"]
                    imageUrl = previewURL.replace("preview.redd.it", "i.redd.it").split("?")[0]
                    submissionData += f"\n{spoilerLink}{imageUrl}{spoilerText}"
            except Exception as e:
                e = e.replace("\n", "\n> ")
                submissionData = f"\n> {e}"
        elif postHint == "hosted:video": # Video post (not stuff like youtube)
            try:
                try:
                    submissionData = submissionJson["secure_media"]["reddit_video"]["fallback_url"]
                except:
                    submissionData = submissionJson["preview"]["reddit_video_preview"]["fallback_url"]
                if "?" in submissionData and spoiler: submissionData += "&?"
                elif spoiler: submissionData += "?"
                else:
                    submissionData = submissionData.split("?source=fallback")[0]
                submissionData = f"\n{spoilerLink}{submissionData}{spoilerText}"
            except Exception as e:
                e = e.replace("\n", "\n> ")
                submissionData = f"\n> {e}\n{spoilerLink}{submissionJson['url']}{spoilerText}"
        elif submissionJson["url"] == "https://www.reddit.com" + submissionJson["permalink"]: # Nothing, should never be used
            submissionData = ""
        elif re.match("https:\/\/www.reddit.com\/r\/[^\s\/]+\/comments\/[^\s\/]+/", submissionJson["url"]) and not crosspost: # Crossposts
            try:
                submissionID = submissionJson["url"].split("/comments/")[1].split("/")[0]
                submission = await self.postJson(submissionID)
                crosspostData = await self.postSubmission(self, message, submission, crosspost=True, forceSpoiler=spoiler)
                crosspostLink = f"\n> \n> Crosspost: <https://redd.it/{submissionID}>\n"
                if len(submissionMetadata) + len(crosspostData) + len(crosspostLink) > 2000:
                    submissionData = crosspostLink + crosspostData[:1956-(len(submissionMetadata)+len(crosspostLink))] + spoilerText + "\n> (Discord max character limit reached)"
                else:
                    submissionData = crosspostLink + crosspostData
            except asyncprawcore.exceptions.NotFound:
                submissionData = f"\n> \n> HTTP error 404 while getting crosspost.\n{spoilerLink}{submissionJson['url']}{spoilerText}"
        else: # Other links
            submissionData = f"\n{spoilerLink}{submissionJson['url']}{spoilerText}"

        if crosspost:
            return submissionMetadata + submissionData
        else:
            await message.channel.send(submissionMetadata + submissionData)
            print(str(message.author)+" NSFW:" + str(submissionJson["over_18"]) +" "+ submissionJson["subreddit_name_prefixed"]+" "+ submissionJson["id"], flush=True)

    async def postJson(submissionID):
        url = "https://reddit.com/" + submissionID + ".json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(str(resp.status))
                response = await resp.text()
                postJson = json.loads(response)
                return postJson[0]["data"]["children"][0]["data"]


# Use old post finder code till i have actually done the new one
# legacyReddit.py (not commited) is reddit.py from before the rewrite
# with only the prawInstance code removed
# # Get post data, crosspost data if it exists.
# try: return postJson[0]["data"]["children"][0]["data"]["crosspost_parent_list"][0]
# except: return postJson[0]["data"]["children"][0]["data"]
import bz2
import os
from legacyReddit import reddit as oldReddit
import asyncpraw, asyncprawcore
class legacyReddit(oldReddit):

    try:
        secrets = keys.read("reddit-client_id", "reddit-client_secret", "reddit-username", "reddit-password")
        prawInstance = asyncpraw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io",
            client_id=secrets[0], client_secret=secrets[1],
            username=secrets[2], password=secrets[3])
    except Exception as e:
        prawInstance = Exception
        prawException = str(e)
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
reddit.exclamationCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":True}]
reddit.exclamationCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":False}]
reddit.exclamationCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":True}]





reddit.mentionedCommands["!r\/([^\s\/]+)(?!\S)"] = [legacyReddit.subreddit, ["message", "commandContent"], {"self":legacyReddit}]
reddit.mentionedCommands["!u\/[A-Za-z0-9_-]+(?!\S)"] = [legacyReddit.user, ["message", "commandContent"], {"self":legacyReddit}]
reddit.exclamationCommands["!r\/([^\s\/]+)(?!\S)"] = [legacyReddit.subreddit, ["message", "commandContent"], {"self":legacyReddit}]
reddit.exclamationCommands["!u\/[A-Za-z0-9_-]+(?!\S)"] = [legacyReddit.user, ["message", "commandContent"], {"self":legacyReddit}]
reddit.startTasks += [legacyReddit.loadRecentSubmissions(legacyReddit)]
reddit.closeTasks += [legacyReddit.saveRecentSubmissions(legacyReddit)]
reddit.closeTasks += [legacyReddit.prawInstance.close()]
