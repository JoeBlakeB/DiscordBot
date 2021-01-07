#!/usr/bin/env python3

import discord
import os
import re
import random
import datetime

try:
    with open("token.txt") as tokenFile:
        token = tokenFile.read().strip()
except:
    token = None
    import sys
    if len(sys.argv) > 1:
        token = sys.argv[1]
    if token == None:
        print("Token not found in token.txt and not in args")
        exit(1)

bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    if re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])
        return

    if message.content.lower() == "git gud":
        await message.channel.send("git: 'gud' is not a git command.")
        return

    if message.content.startswith("<@!"+str(bot.user.id)+">"):
        await botMentioned(message)
        return

class botMentioned:
    from btec import btec, unit
    from stuff import good, git

    async def __new__(self, message):
        command = message.content.strip()
        while "__" in command: command.replace("__", "")
        while "  " in command: command = command.replace("  ", " ")
        command = command.split()

        try:
            commandattr = getattr(self, command[1].lower())
            await commandattr(message, command)
        except IndexError:
            await self.__command_not_found__(message, command)
        except KeyError:
            await self.__command_not_found__(message, command)
        except AttributeError:
            await self.__command_not_found__(message, command)
        except Exception as e:
            await message.channel.send("something went wrong:\n"+str(e))

    class help:
        helpMessageShort = "short help"
        helpMessageLong  = "LONG HELP"
        commandClasses = ""
        async def __new__(self, message, command):
            if self.commandClasses == "":
                for commandClass in dir(botMentioned):
                    if "__" not in commandClass:
                        try:
                            if getattr(botMentioned, commandClass).helpMessageShort != None:
                                self.commandClasses += commandClass + ", "
                        except: pass
                self.commandClasses = self.commandClasses[:-2]
            await message.channel.send("Available commands: " + self.commandClasses)

    class __command_not_found__:
        noCommandSpecified = ["wat?", "wat", "?", "the fuck you want?"]
        commandNotFound = ["{name}: {command[1]}: command not found", "what do you mean {message}"]
        async def __new__(self, message, command):
            if len(command) < 2:
                await message.channel.send(random.choice(self.noCommandSpecified))
            else:
                await message.channel.send(random.choice(self.commandNotFound + self.noCommandSpecified)
                    .format(name = message.channel.guild.me.display_name, command = command, message = ' '.join(command[1:])))

    def __terminate_threads__():
        for commandClass in dir(botMentioned):
            if "__" not in commandClass:
                try:
                    if getattr(botMentioned, commandClass).terminate != None:
                        getattr(botMentioned, commandClass).terminate = True
                except: pass

bot.run(token)
botMentioned.__terminate_threads__()
