#!/usr/bin/env python3

import random
import discord

class good:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() == "bot":
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception
class bad:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() == "bot":
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
