import asyncpraw, asyncprawcore
import datetime
import discord

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

    async def reddit(self, message):
        return await message.add_reaction("❌")

    async def subreddit(self, message):
        return await message.add_reaction("❌")

    async def user(self, message):
        return await message.add_reaction("❌")

    async def url(self, message):
        bruh = time.time()
        submission = await self.prawInstance.submission(id=message.content.split(" ")[-1])
        print(time.time()-bruh)
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
                awards += "⠀" + emojis["Coin"] + " {0:,}".format(coinCount)
        stats = emojis["Upvote"]+" {0:,}⠀🗨 {1:,}{2}\n> 🗓 {3}".format(submission.score, submission.num_comments, awards,
            datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M"))

        submissionMetadata = f"> {title}\n> <https://redd.it/{submission.id}>\n> {author}{extras}\n> {stats}"

        if spoiler:
            spoilerLink = "||"
            spoilerText = "||"
        else:
            spoilerLink = "> "
            spoilerText = ""

        if submission.is_self and submission.selftext != "": # Text post
            if spoiler:
                submissionData = "\n> " + spoilerText + submission.selftext.replace("\n", "\n> ").replace("|", "¦") + spoilerText
            else:
                submissionData = "\n> " + submission.selftext.replace("\n", "\n> ")
            if len(submissionMetadata) + len(submissionData) > 2000:
                submissionData = submissionData[:1956-len(submissionMetadata)] + spoilerText + "\n> (Discord max character limit reached)"
        else: # Other links
            if submission.url != "https://www.reddit.com" + submission.permalink:
                submissionData = f"\n{spoilerLink}{submission.url}{spoilerText}"
            else:
                submissionData = ""



        await message.channel.send(submissionMetadata + submissionData)
        print(str(message.author)+" NSFW:" + str(submission.over_18) +" "+ submission.subreddit.display_name+" "+ submission.id)


reddit.mentionedCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message"], {"self":reddit}]
reddit.mentionedCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.user, ["message"], {"self":reddit}]
reddit.mentionedCommands["(https:\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message"], {"self":reddit}]
reddit.exclamationCommands["reddit(?!\S)"] = [reddit.reddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["r\/([^\s\/]+)(?!\S)"] = [reddit.subreddit, ["message"], {"self":reddit}]
reddit.exclamationCommands["u\/[A-Za-z0-9_-]+(?!\S)"] = [reddit.user, ["message"], {"self":reddit}]
reddit.exclamationCommands["(https:\/\/|)(www.|)redd(.it|it.com)\/"] = [reddit.url, ["message"], {"self":reddit}]
reddit.closeTasks += [reddit.prawInstance.close()]
