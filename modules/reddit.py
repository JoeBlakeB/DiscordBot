import aiohttp
import asyncio
import bz2
import datetime
import discord
import json
import re
import os
import time
import traceback
import urllib.parse

import baseClass
import keys

emojis = {
    "RedditGold":   "<:RedditGold:829118524969975809>",
    "Upvote":       "<:upvote:829141166430748724>",
    "Coin":         "<:Coin:829274378881073174>",
    "Four":         "<:four:877965699765665832>"
}

class reddit(baseClass.baseClass):
    redditHelp = {"title":"JoeBot Reddit", "description":("To get posts from reddit:\n<@!796433833296658442> r/<SUBREDDIT>\nor\n!r/<SUBREDDIT>"+
        "\n\nYou can sort by different methods like top/new:\n<@!796433833296658442> r/<SUBREDDIT> top"+
        "\n\nYou can also define the time range for those searches:\n<@!796433833296658442> r/<SUBREDDIT> top month"+
        "\n\nIf you want to search for a post, say search then say the search terms:\n<@!796433833296658442> r/<SUBREDDIT> search <SEARCH TERMS>"+
        "\n\nTo get posts from users instead of subreddits just say u/ instead of r/"+
        "\n\nTo use JoeBot in DMs, remove the prefix, for example r/<SUBREDDIT> instead of !r/<SUBREDDIT>"),
        "thumbnail":"https://cdn.discordapp.com/emojis/690344425356001320.png"}
    async def reddit(self, message):
        embed = discord.Embed()
        embed.title = reddit.redditHelp["title"]
        embed.description = reddit.redditHelp["description"]
        embed.set_thumbnail(url=reddit.redditHelp["thumbnail"])
        await message.channel.send(embed=embed)

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
                break
        else:
            sortTime = self.sortTimes[0]

        try:
            isNSFW = message.channel.is_nsfw()
        except:
            isNSFW = True

        # Convert that to a URL
        url = f"https://www.reddit.com/{('user'*int(not isSubreddit))+('r'*int(isSubreddit))}/{subredditName}/{'submitted/'*int(not isSubreddit)}"
        if search:
            url += f"search.json?q={urllib.parse.quote(searchTerm, safe='')}&restrict_sr=1&sort={sortMethod}&t={sortTime}{'&include_over_18=on'*int(isNSFW)}&limit=30"
        else:
            url += f"{sortMethod}.json?t={sortTime}{'&include_over_18=on'*int(isNSFW)}&limit=30"

        # check cache and if its in cache, use that instead of requesting again
        getNewPost = not await self.cache.tryCache(self, message, url, isNSFW)

        # Get the search from the URL
        if getNewPost:
            try:
                posts, history = await self.getListing(self, url)
                posts = posts["data"]
            except Exception as e:
                if str(e) in ["403", "404"]:
                    try:
                        reason = ""
                        reasonMessageName = "description"
                        reasonJson = (await self.getListing(self, f"https://gateway.reddit.com/desktopapi/v1/subreddits/{subredditName}?{'&include_over_18=on'*int(isNSFW)}", anyStatus=True))[0]
                        print(reasonJson)
                        if reasonJson["reason"].lower() == "private":
                            reason = "because it is set to private."
                        elif reasonJson["reason"].lower() == "quarantined":
                            reason = "because it has been quarantined and a reddit account with verified email is required to view it."
                            reasonMessageName = "quarantineMessage"
                        elif reasonJson["reason"].lower() == "banned":
                            reason = f"because {'they have'*int(not isSubreddit)}{'it has'*int(isSubreddit)} been banned."
                            reasonMessageName = "ban_message"
                        if reasonJson["data"][reasonMessageName] != "":
                            reason += "\n> " + (reasonJson["data"][reasonMessageName].replace("\n\n", "\n").replace("\n", "\n> ")
                                .replace("](", ": ").replace("[", "").replace(")", ""))
                    except: pass
                    await message.channel.send(f"Could not get a post from that {'user'*int(not isSubreddit)}{'subreddit'*int(isSubreddit)} {reason}")
                else:
                    await message.channel.send("Error: " + str(e))
                return

            # If the subreddit does not exist
            if history:
                if len(posts["children"]) == 0:
                    await message.channel.send(f"That {'user'*int(not isSubreddit)}{'subreddit'*int(isSubreddit)} does not exist.")
                elif len(posts["children"]) == 1 and posts["children"][0]["kind"] == "t5":
                    await message.channel.send(f"That {'user'*int(not isSubreddit)}{'subreddit'*int(isSubreddit)} does not exist, did you mean {posts['children'][0]['data']['display_name_prefixed']}?")
                else:
                    listOfReccomendations = []
                    for sub in posts["children"]:
                        if sub["kind"] == "t5": listOfReccomendations.append(sub["data"]["display_name_prefixed"])
                    await message.channel.send(f"That {'user'*int(not isSubreddit)}{'subreddit'*int(isSubreddit)} does not exist, did you mean?\n - " + "\n - ".join(listOfReccomendations))
                return

        # Select post to send to channel
        nsfwBlock = [0, False] # sfw, nsfw
        while getNewPost:
            allListings = [posts]
            try:
                for post in posts["children"]:
                    if self.recentPosts.check(post["data"]["id"], str(message.channel.id)) and not (post["data"]["stickied"] and not (
                            "pinned" in message.content.lower() or "stickied" in message.content.lower())):
                        if post["data"]["over_18"] and not isNSFW:
                            nsfwBlock[1] = True
                        else:
                            self.recentPosts.append(post["data"]["id"], str(message.channel.id))
                            await self.postSubmission(self, message, post["data"])
                            self.cache.addToCache(self, url, sortMethod, allListings)
                            break
                    elif not post["data"]["over_18"] and not isNSFW:
                        nsfwBlock[0] += 1
                else:
                    # Try next page
                    # only if there are enough sfw posts in results if its a sfw channel
                    if (nsfwBlock[0] >= len(posts) / 3) or isNSFW:
                        if posts["after"] != None:
                            nsfwBlock[1] = False
                            await message.channel.trigger_typing()
                            nextPage, redirects = await self.getListing(self, url.replace("limit=30", "limit=100")+"&after="+posts["after"])
                            nextPage = nextPage["data"]
                            if len(nextPage["children"]) != 0:
                                posts = nextPage
                                allListings.append(posts)
                                continue
                    await message.channel.send(f"Could not get a{'nother'*int(bool(len(posts['children'])) and not nsfwBlock[1])}{' SFW'*int(nsfwBlock[1])} post from that {'user'*int(not isSubreddit)}{'subreddit'*int(isSubreddit)}{' with that search'*int(search)}.{' Try using JoeBot in a NSFW channel or in your DMs to view these posts.'*int(nsfwBlock[1])}")
                break
            except:
                await message.channel.send("An error has occured while trying to get a post from that sub.")
                print("An error has occured while trying to get", url, traceback.format_exc(), flush=True)
                break
        self.cache.cleanCache(self)
        await self.recentPosts.autosave()

    async def getListing(self, url, anyStatus=False):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200 and not anyStatus:
                    raise Exception(str(resp.status))
                response = await resp.text()
        responseJson = json.loads(response)
        return responseJson, bool(resp.history)

    async def url(self, message, messageContentLower, exclamation):
        try:
            try:
                await message.edit(suppress=True)
            except: pass
            # get id from url
            messageContentLower = messageContentLower[7-(6*int(exclamation)):]
            messageContentLower = messageContentLower.replace("https://", "").replace("http://", "").replace("www.", "")
            if messageContentLower[:8] == "redd.it/":
                submissionID = messageContentLower[8:].split(" ")[0]
            else:
                submissionID = messageContentLower.split("/comments/")[1].split("/")[0]
            # get post from id
            submissionJson = await self.postJson(submissionID)
        except Exception as e:
            await message.add_reaction("⚠️")
            if str(e) == "403": react = ["4️⃣", "0️⃣", "3️⃣"]
            elif str(e) == "404": react = ["4️⃣", "0️⃣", emojis["Four"]]
            else: react = []
            for emoji in react:
                await message.add_reaction(emoji)
            return
        try:
            isNSFW = message.channel.is_nsfw()
        except:
            isNSFW = True
        if submissionJson["over_18"] and not isNSFW:
            await message.channel.send("That post is blocked because you are in a SFW channel.")
        else:
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
        elif re.match("(https:\/\/www.reddit.com|)\/r\/[^\s\/]+\/comments\/[^\s\/]+/", submissionJson["url"]) and not crosspost: # Crossposts
            if submissionJson["url"][:3] == "/r/":
                submissionJson["url"] = "https://www.reddit.com" + submissionJson["url"]
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

    async def postJson(submissionID):
        url = "https://reddit.com/" + submissionID + ".json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(str(resp.status))
                response = await resp.text()
                postJson = json.loads(response)
                return postJson[0]["data"]["children"][0]["data"]

    class recentPosts:
        recentPosts = {}
        # {"ChannelID":{"DayOfYear":[PostIDs]}}
        botLastUsed = 0
        autoSaveWaiting = False

        def check(postID, channelID):
            try:
                for day in list(reddit.recentPosts.recentPosts[channelID].values()):
                    if postID in day:
                        return False
            except: pass
            return True

        def append(postID, channelID):
            try:
                reddit.recentPosts.recentPosts[channelID][datetime.datetime.utcnow().strftime("%Y%m%d")].append(postID)
            except:
               try:
                   reddit.recentPosts.recentPosts[channelID][datetime.datetime.utcnow().strftime("%Y%m%d")] = [postID]
               except:
                  reddit.recentPosts.recentPosts[channelID] = {datetime.datetime.utcnow().strftime("%Y%m%d"):[postID]}

        def clean():
            for channel in list(reddit.recentPosts.recentPosts):
                for date in list(reddit.recentPosts.recentPosts[channel]):  # keep posts in the list for two weeks before removing them
                    if (datetime.date.today() - (datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])))).days >= 14:
                        del reddit.recentPosts.recentPosts[channel][date]
                if reddit.recentPosts.recentPosts[channel] == {}:
                    del reddit.recentPosts.recentPosts[channel]

        async def load():
            try:
                with bz2.open("tmp/recentSubmissions.txt.bz2", "rb") as recentSubmissionsFile:
                    reddit.recentPosts.recentPosts = json.loads(str(recentSubmissionsFile.read(), "utf-8"))
            except FileNotFoundError:
                try:
                    with bz2.open("tmp/recentSubmissions.txt.bz2.bak", "rb") as recentSubmissionsFile:
                        reddit.recentPosts.recentPosts = json.loads(str(recentSubmissionsFile.read(), "utf-8"))
                except FileNotFoundError: pass
            reddit.recentPosts.clean()

        async def save():
            os.makedirs("tmp", exist_ok=True)
            try: os.rename("tmp/recentSubmissions.txt.bz2", "tmp/recentSubmissions.txt.bz2.bak")
            except: pass
            with bz2.open("tmp/recentSubmissions.txt.bz2", "wb") as recentSubmissionsFile:
                recentSubmissionsFile.write(bytes(json.dumps(reddit.recentPosts.recentPosts, indent=4), "utf-8"))
            try: os.remove("tmp/recentSubmissions.txt.bz2.bak")
            except: pass

        async def autosave():
            reddit.recentPosts.botLastUsed = time.time()
            if reddit.recentPosts.autoSaveWaiting:
                return

            reddit.recentPosts.autoSaveWaiting = True
            while reddit.recentPosts.botLastUsed + 600 >= time.time():
                await asyncio.sleep(300)
            reddit.recentPosts.clean()
            await reddit.recentPosts.save()
            reddit.recentPosts.autoSaveWaiting = False

    class cache:
        cache = {}
        # {"url": [listOfPostJsons, expiresTimestamp]}
        keepInCacheTime = {"hot":600, "new":60, "rising":180, "top":1800, "controversial":900, "relevant": 1200}

        async def tryCache(self, message, url, isNSFW):
            try:
                if time.time() > self.cache.cache[url][1]:
                    return False
                for post in self.cache.cache[url][0]:
                    if self.recentPosts.check(post["id"], str(message.channel.id)) and not (post["stickied"] and not (
                            "pinned" in message.content.lower() or "stickied" in message.content.lower())) and not (post["over_18"] and not isNSFW):
                        self.recentPosts.append(post["id"], str(message.channel.id))
                        await self.postSubmission(self, message, post)
                        return True
            except: pass
            return False

        def addToCache(self, url, sortMethod, allListings):
            posts = []
            for listing in allListings:
                for post in listing["children"]:
                    posts.append(post["data"])
            self.cache.cache[url] = [posts, time.time() + self.cache.keepInCacheTime[sortMethod]]

        def cleanCache(self):
            timeNow = time.time()
            for url in list(self.cache.cache):
                if timeNow > self.cache.cache[url][1]:
                    del self.cache.cache[url]

reddit.mentionedCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":True}]
reddit.mentionedCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":False}]
reddit.mentionedCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":False}]
reddit.exclamationCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":True}]
reddit.exclamationCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.subreddit, ["message", "commandContent"], {"self":reddit, "isSubreddit":False}]
reddit.exclamationCommands["(http(s|):\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message", "messageContentLower"], {"self":reddit, "exclamation":True}]
reddit.startTasks += [reddit.recentPosts.load()]
reddit.closeTasks += [reddit.recentPosts.save()]
reddit.help["reddit"] = ["embed,include", reddit.redditHelp]
