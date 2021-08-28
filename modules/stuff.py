import asyncio
import discord
import random
import re
import time

import baseClass

emojis = {
    "HoodCate":     "<:hoodcate:822937989667749918>",
    "HoodCateHD":   "<:hoodcateHD:822937932464914494>",
    "Shotgun1":     "<:shotgun1:803767806956929055>",
    "Shotgun2":     "<:shotgun2:803767806914068493>",
    "Shotgun3":     "<:shotgun3:803767807124439061>",
    "Shotgun4":     "<a:shotgun4:803767807170576384>",
    "RedditGold":   "<:RedditGold:829118524969975809>",
    "Upvote":       "<:upvote:829141166430748724>",
    "Coin":         "<:Coin:829274378881073174>",
    "Four":         "<:four:829673449110765598>",
    "TeaTime":      "<a:teatime:834903558599213057>",
    "TeaTime2":     "<a:teatime2:835602583057203200>",
    "Amogus":       "<:amogus:811622676783169536>",
    "SidStare":     "<a:SidStare:822896085856157756>",
    "CatStand":     "<:CatStand:814251218033180743>",
    "TigerBoop":    "<a:tigerboop:808399700549697596>"
}

class stuff(baseClass.baseClass, baseClass.baseUtils):
    emojiRegex = re.compile("<(a|)(:|;)(.*)(:|;)(\d*)>")
    async def say(message):
        messageContent = "say ".join(message.content.split("say ")[1:])
        if (len(messageContent) >= 128 and ("\n>" in messageContent)) or len(messageContent) >= 1024:
            return await message.add_reaction("❌")
        if stuff.emojiRegex.search(messageContent):
            await message.channel.send(messageContent.replace(";", ":"))
        else:
            await message.channel.send(messageContent)

    async def kill(message):
        whoToKill = "kill ".join(message.content.split("kill ")[1:]).split(" as ")[0]
        if len(whoToKill) > 256:
            return await message.add_reaction("❌")

        if " as " in message.content:
            murderer = message.content.split(" as ")[-1]
        else:
            murderer = "<@"+str(message.author.id)+">"
        gun = " " + emojis["Shotgun1"] + emojis["Shotgun2"] + emojis["Shotgun3"] + emojis["Shotgun4"] + " "

        if stuff.emojiRegex.search(murderer + gun + whoToKill):
            await message.channel.send((murderer + gun + whoToKill).replace(";", ":"))
        else:
            await message.channel.send(murderer + gun + whoToKill)

    async def goodBot(message):
        if "good" in message.content:
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            await message.channel.send(random.choice(["ÓnÒ why am I a bad bot?", "ÒwÓ no you", "thats mean"]))

    youKnowIHadToDoItToEmBody = "\n<:YouKnowIHadToL2:832746970283245588><:YouKnowIHadToC2:832746970103283762><:YouKnowIHadToR2:832746969906675753>\n<:YouKnowIHadToL3:832746969679134731><:YouKnowIHadToC3:832746969964609546><:YouKnowIHadToR3:832746970103676938>\n<:YouKnowIHadToL4:832746969986236457><:YouKnowIHadToC4:832746969566937140><:YouKnowIHadToR4:832746970254671902>"
    youKnowLeft = "<:YouKnowIHadToL1:832746970544078889>"
    youKnowRight = "<:YouKnowIHadToR1:832746970001965056>"
    async def youKnowIHadToDoItToEm(message, messageContentLower, bot, mentioned=0):
        try:
            text = messageContentLower[23+mentioned:].strip()
        except:
            text = ""
        try:
            if stuff.emojiRegex.match(text):
                id = int(text.replace(";", ":").split(":")[-1][:-1])
                head = bot.client.get_emoji(id)
            else:
                try:
                    id = int(text)
                    head = bot.client.get_emoji(id)
                except:
                    head = discord.utils.get(message.guild.emojis, name=text)
        except: head = None
        if head == None:
            head = "<:YouKnowIHadToC1:832746969822527509>"
            if len(text) != 0:
                await message.add_reaction("❌")
        await message.channel.send(stuff.youKnowLeft + str(head) + stuff.youKnowRight + stuff.youKnowIHadToDoItToEmBody)

    async def tomato(message):
        if isinstance(message.channel, discord.channel.DMChannel):
            await asyncio.sleep(random.randint(10,40))
            await message.channel.send(message.author.display_name + " has been infected with a tomato")
            await asyncio.sleep(random.randint(5,20))
            await message.channel.send("Now change your status to \"DM me the word tomato\" to infect others")

        else:
            await message.add_reaction("🍅")

    async def pfp(message, bot):
        try:
            userID = message.content.split(" ")[-1]
            userID = re.findall(r"\d+", userID)[0]
            user = bot.client.get_user(int(userID))
            await message.channel.send(user.avatar_url)
        except Exception:
            try:
                await message.channel.send(message.author.avatar_url)
            except Exception:
                await message.add_reaction("⚠️")

stuff.mentionedCommands["say(?!\S)"] = [stuff.say, ["message"], {}]
stuff.mentionedCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.exclamationCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.mentionedCommands["(good|bad)( |)(bot|boy)$"] = [stuff.goodBot, ["message"], {}]
stuff.exclamationCommands["youknowihadtodoitto(th|)em(?!\S)"] = [stuff.youKnowIHadToDoItToEm, ["message", "messageContentLower", "bot"], {}]
stuff.mentionedCommands["youknowihadtodoitto(th|)em(?!\S)"] = [stuff.youKnowIHadToDoItToEm, ["message", "messageContentLower", "bot"], {"mentioned": 6}]
stuff.mentionedCommands["pfp(?!\S)"] = [stuff.pfp, ["message", "bot"], {}]
stuff.exclamationCommands["pfp(?!\S)"] = [stuff.pfp, ["message", "bot"], {}]

stuff.mentionedCommands["tomato"] = [stuff.tomato, ["message"], {}]

stuff.help["kill"] = ["include"]
