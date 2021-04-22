import asyncio
import random

import baseClass
from emojis import emojis

class stuff(baseClass.baseClass, baseClass.baseUtils):
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

stuff.mentionedCommands["say(?!\S)"] = [stuff.say, ["message"], {}]
stuff.mentionedCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.exclamationCommands["kill(?!\S)"] = [stuff.kill, ["message"], {}]
stuff.mentionedCommands["porn(?!\S)"] = [stuff.porn, ["message"], {}]
stuff.mentionedCommands["(good|bad)( |)(bot|boy)$"] = [stuff.goodBot, ["message"], {}]
