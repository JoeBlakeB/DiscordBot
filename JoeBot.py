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
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(name="@JoeBot unit #"))

@bot.event
async def on_message(message):
    if message.author.name == "MEE6" and "365154655313068032" in message.content:
        await message.channel.send("<@!365154655313068032> has told me to tell you to fuck off")

    if message.author == bot.user or message.author.bot:
        return

    if re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])
        return

    if "kev" in message.content.lower():
        emoji = discord.utils.get(message.channel.guild.emojis, name='xander')
        await message.add_reaction(emoji)
        return

    if message.content.lower() == "git gud":
        await message.channel.send("git: 'gud' is not a git command.")
        return

    if (message.content.startswith("<@!"+str(bot.user.id)+">") or
            message.content.startswith("<@"+str(bot.user.id)+">")):
        await botMentioned(message)
        return

    elif ("<@!"+str(bot.user.id)+">" in message.content or
            "<@"+str(bot.user.id)+">" in message.content):
        await botMentioned.__command_not_found__(message, [])

class botMentioned:
    from help import help
    from btec import btec, unit
    from stuff import good, git

    async def __new__(self, message):
        command = message.content.strip()
        while "__" in command: command.replace("__", "")
        while "  " in command: command = command.replace("  ", " ")
        command = command.split()

        try:
            commandattr = getattr(self, command[1].lower())
            await commandattr(message, command, self)
        except IndexError:
            await self.__command_not_found__(message, command)
        except KeyError:
            await self.__command_not_found__(message, command)
        except AttributeError:
            await self.__command_not_found__(message, command)
        except Exception as e:
            await message.channel.send("something went wrong:\n"+str(e))

    class __command_not_found__:
        noCommandSpecified = ["wat?", "wat", "?", "the fuck you want?"]
        commandNotFound = ["what do you mean {message}"]
        async def __new__(self, message, command):
            if len(command) < 2:
                await message.channel.send(random.choice(self.noCommandSpecified))
            else:
                await message.channel.send(random.choice(self.commandNotFound + self.noCommandSpecified)
                    .format(message = ' '.join(command[1:])))

    def __embedColor__():
        return 0x000000

    def __terminate_threads__():
        for commandClass in dir(botMentioned):
            if "__" not in commandClass:
                try:
                    if getattr(botMentioned, commandClass).terminate != None:
                        getattr(botMentioned, commandClass).terminate = True
                except: pass

bot.run(token, reconnect=True)
botMentioned.__terminate_threads__()
