#!/usr/bin/env python3

import random

class good:
    async def __new__(self, message, command):
        if command[2].lower() == "bot":
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception

class git:
    async def __new__(self, message, command):
        if command[2].lower() == "gud":
            await message.channel.send("git: 'gud' is not a git command. See 'git help'.")
        elif command[2].lower()[-4:] == "help":
            await message.channel.send("no get fucked ÒωÓ")
        elif command[2].lower() == "clone":
            try:
                await message.channel.send("Cloning into '"+command[3]+"'...")
                await message.channel.send("Password for '"+command[3]+"':")
            except:
                await message.channel.send("fatal: You must specify a repository to clone.")
        else:
            raise Exception
