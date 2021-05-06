import asyncio
import random
import re

import baseClass
from emojis import emojis

class stuff(baseClass.baseClass, baseClass.baseUtils):
    emojiRegex = re.compile("<(a|)(:|;)(.*)(:|;)(\d*)>")
    lowerEmojis = {}
    for emoji in emojis:
        lowerEmojis[emoji.lower()] = emojis[emoji]
    async def say(message):
        messageContent = "say ".join(message.content.split("say ")[1:])
        if len(messageContent) >= 256:
            return await message.add_reaction("❌")
        sayContent = ""
        emojiName = None
        for i in range(len(messageContent)):
            if emojiName != None and messageContent[i] == ":":
                if emojiName in list(emojis):
                    sayContent = sayContent[:(-1)-len(emojiName)] + emojis[emojiName]
                else:
                    emojiName += ":"
                emojiName = None
            elif emojiName == None and messageContent[i] == ":":
                emojiName = ""
                sayContent += messageContent[i]
            else:
                if emojiName != None:
                    emojiName += messageContent[i]
                sayContent += messageContent[i]
        if stuff.emojiRegex.search(sayContent):
            await message.channel.send(sayContent.replace(";", ":"))
        else:
            await message.channel.send(sayContent)
        print(str(message.author)+" said \"" + sayContent + "\"", flush=True)
        await stuff.deleteMessage(message)

    async def kill(message):
        whoToKill = "kill ".join(message.content.split("kill ")[1:]).split(" as ")[0]
        if len(whoToKill) > 64:
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
        print(str(message.author)+" killed \"" + whoToKill + "\"", flush=True)
        await stuff.deleteMessage(message)

    bitlyUrls = ["3chJDM7", "3t3GQvM", "36gTVIs", "36kYhyj", "2KWKKWh", "2MeJUVt", "3iVIj2F", "2YpG522",
        "2NIS6Oa", "2Yl6zBI", "3qVKCFR", "3iVUpJc", "3j6gXap", "3ae9aD1", "2YkFTRB", "3cic5xi",
        "3pvyOtI", "39nIz7x", "3r3UOfB", "36C2Nsz", "39mMKjT", "36nD07g", "3t7GSmG", "3oxL5MY",
        "3oqE8gC", "3ahTgrE", "3iTpTQ0", "2YtoPZH", "3t5V3sk"]
    async def porn(message):
        await message.channel.send("<https://bit.ly/" + random.choice(stuff.bitlyUrls) + ">")

    async def goodBot(message):
        if "good" in message.content:
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            await message.channel.send(random.choice(["ÓnÒ why am I a bad bot?", "ÒwÓ no you", "thats mean"]))

    youKnowIHadToDoItToEmBody = "\n<:YouKnowIHadToL2:832746970283245588><:YouKnowIHadToC2:832746970103283762><:YouKnowIHadToR2:832746969906675753>\n<:YouKnowIHadToL3:832746969679134731><:YouKnowIHadToC3:832746969964609546><:YouKnowIHadToR3:832746970103676938>\n<:YouKnowIHadToL4:832746969986236457><:YouKnowIHadToC4:832746969566937140><:YouKnowIHadToR4:832746970254671902>"
    youKnowLeft = "<:YouKnowIHadToL1:832746970544078889>"
    youKnowRight = "<:YouKnowIHadToR1:832746970001965056>"
    async def youKnowIHadToDoItToEm(message, messageContentLower):
        try:
            text = messageContentLower[23:].strip()
        except:
            text = ""
        if len(text) >= 64:
            return await message.add_reaction("❌")
        if len(text) == 0:
            return await message.channel.send(stuff.youKnowIHadToDoItToEmBody[1:])
        if text in ["orig", "original"]:
            head = "<:YouKnowIHadToC1:832746969822527509>"
        elif text == "random":
            head = random.choice(list(emojis.values()))
        elif text.replace(":", "") in stuff.lowerEmojis:
            head =  + stuff.lowerEmojis[text.replace(":", "")]
        else:
            if stuff.emojiRegex.match(text):
                head = text.replace(";", ":")
            else:
                head = text
        await message.channel.send(stuff.youKnowLeft + head + stuff.youKnowRight + stuff.youKnowIHadToDoItToEmBody)
        print(str(message.author)+" youknowihadtodoittoem \"" + head + "\"", flush=True)
        await stuff.deleteMessage(message)

stuff.mentionedCommands["say(?!\S)"] = [stuff.say, ["message"], {}]
stuff.mentionedCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.exclamationCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.mentionedCommands["porn(?!\S)"] = [stuff.porn, ["message"], {}]
stuff.mentionedCommands["(good|bad)( |)(bot|boy)$"] = [stuff.goodBot, ["message"], {}]
stuff.exclamationCommands["youknowihadtodoitto(th|)em(?!\S)"] = [stuff.youKnowIHadToDoItToEm, ["message", "messageContentLower"], {}]
stuff.exclamationCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
