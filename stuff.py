#!/usr/bin/env python3

import random
import discord
import asyncio

class good:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() in ["bot", "boy"]:
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception
class bad:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() in ["bot", "boy"]:
            await message.channel.send(random.choice(["ÓnÒ why am I a bad bot?", "ÒwÓ no you", "thats mean"]))
        else:
            raise Exception

class hi:
    async def __new__(self, message, command, parentClass):
        await message.channel.send(random.choice(["Hello", "Hi", "Hey", "uwu hi", ":3 hey", "Hello there", "Hewwo"]))

hey = hi
hello = hi

class say:
    async def __new__(self, message, command, parentClass):
        if len(command) <= 2:
            raise IndexError
            return
        await message.channel.send(" ".join(command[2:]))

class gun:
    async def __new__(self, message, command, parentClass):
        await message.channel.send(self.gun(parentClass))
    def gun(parentClass):
        bot = parentClass.__bot__()
        gun = ""
        for i in range(1,5):
            gun += str(discord.utils.get(bot.emojis, name="shotgun"+str(i)))
        return gun

class kill:
    help = {"list": True, "ListPriority": 10, "Title":"Kill",
        "ShortHelp": "Kill someone *@{displayName} kill <name>*",
        "LongHelp": "Kill someone.\n"+
        "Use **@{displayName} kill <name>**"}
    async def __new__(self, message, command, parentClass):
        if len(command) <= 2:
            await message.channel.send("You need to say who you want to kill.")
            return
        await message.channel.send(message.author.display_name + " " + gun.gun(parentClass) + " " + " ".join(command[2:]))

class pogchamp:
    async def __new__(self, message, command, parentClass):
        for i in range(random.randint(4,16)):
            await message.channel.send("PogChamp")
            await asyncio.sleep(2)

class porn:
    help = {"list": False, "Title":"Porn",
        "LongHelp": "Porn.\n"+
        "Use **@{displayName} porn**"}
    urls = ["3chJDM7", "3t3GQvM", "36gTVIs", "36kYhyj", "2KWKKWh", "2MeJUVt", "3iVIj2F", "2YpG522",
        "2NIS6Oa", "2Yl6zBI", "3qVKCFR", "3iVUpJc", "3j6gXap", "3ae9aD1", "2YkFTRB", "3cic5xi",
        "3pvyOtI", "39nIz7x", "3r3UOfB", "36C2Nsz", "39mMKjT", "36nD07g", "3t7GSmG", "3oxL5MY",
        "3oqE8gC", "3ahTgrE", "3iTpTQ0", "2YtoPZH", "3t5V3sk"]
    async def __new__(self, message, command, parentClass):
        embed = discord.Embed()
        embed.title = random.choice(["Here you go.", "Keep the change you filthy animal", "Here, now fuck off.", "Fine"])
        embed.color = parentClass.__embedColor__()
        embed.url = "https://bit.ly/" + random.choice(self.urls)
        await message.channel.send(embed=embed)
