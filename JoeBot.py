#!/usr/bin/env python3

import discord
import os
import re
import random
import datetime
import threading

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
    await bot.change_presence(activity=discord.Game(name="@JoeBot help"))

@bot.event
async def on_message(message):
    if message.author.name == "MEE6" and "365154655313068032" in message.content:
        await message.channel.send("<@!365154655313068032> has told me to tell you to fuck off")

    if message.author == bot.user or message.author.bot:
        return

    elif re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])

    elif "kev" in message.content.lower().split():
        emoji = discord.utils.get(message.channel.guild.emojis, name='xander')
        await message.add_reaction(emoji)

    if message.content.lower() == "git gud":
        await message.channel.send("git: 'gud' is not a git command.")

    elif (message.content.startswith("<@!"+str(bot.user.id)+">") or
            message.content.startswith("<@"+str(bot.user.id)+">")):
        await botMentioned(message)

    elif ("<@!"+str(bot.user.id)+">" in message.content or
            "<@"+str(bot.user.id)+">" in message.content):
        await botMentioned.__command_not_found__(message, [])

    elif "69" in message.content.split():
        await message.channel.send("Nice.")

class botMentioned:
    from help import help
    from btec import unit
    from stuff import good

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

    async def __long_send__(message, embed):
        await message.channel.send(embed=embed)
        ## TODO: handle description being above 2048 chars

    def __embedColor__():
        return random.choice([0xFF0000, 0x00FF00, 0x0000FF])

def startThreads():
    for thread in threads:
        threads[thread].start()

threads = {"unitSetup": threading.Thread(target = botMentioned.unit.setup, args = (botMentioned.unit,))}
startThreads()
bot.run(token, reconnect=True)
