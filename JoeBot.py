#!/usr/bin/env python3

import discord
import os
import sys
import re
import random
import datetime
import threading
import asyncio

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

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

botPresenceRunning = False
async def botPresence():
    songs = ["C418 - Dog", "C418 - Cat", "C418 - Blocks", "C418 - Strad", "C418 - Wait", "C418 - Living Mice",
             "C418 - Chirp", "C418 - Mice On Venus", "C418 - Aria Math", "C418 - Subwoofer Lullaby"]
    botPresenceRunning = True
    while True:
        try:
            now = datetime.datetime.now()
            timeNow = int(str(now.hour)+("0"+str(now.minute))[-2:])
            if now.weekday() in [0, 2, 4] and timeNow >= 845 and timeNow <= 1600:
                await bot.change_presence(activity=discord.Activity(name="@JoeBot help", type=2))
            else:
                await bot.change_presence(activity=discord.Activity(name=random.choice(songs), type=2))
            await asyncio.sleep(random.randint(200, 300))
        except:
            botPresenceRunning = False
            return

joinMessages = ["I should probably warn you that {name} is a registered sex offender."]
leaveMessages = ["{name} leaving is kinda poggers."]

def userJoinLeave(member, messageList):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel == None:
        channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel == None:
        return None, None
    else:
        return channel, random.choice(messageList).format(name=member.display_name)

@bot.event
async def on_member_join(member):
    channel, message = userJoinLeave(member, joinMessages)
    if channel != None:
        await channel.send(message)

@bot.event
async def on_member_remove(member):
    channel, message = userJoinLeave(member, leaveMessages)
    if channel != None:
        await channel.send(message)

@bot.event
async def on_ready():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Logged in as {0.user}".format(bot))
    if not botPresenceRunning:
        asyncio.create_task(botPresence())

@bot.event
async def on_message(message):
    if message.author.name == "MEE6":
        if "365154655313068032" in message.content and "you just wasted more of your life typing" in message.content:
            await message.channel.send("<@!365154655313068032> has told me to tell you to fuck off")
        return

    if message.author == bot.user or message.author.bot:
        return

    if re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])

    elif "kev" in message.content.lower():
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
    from stuff import good, bad
    from stats import stats

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

    def __bot__():
        global bot
        return bot

def startThreads():
    for thread in threads:
        threads[thread].start()

print("Python Version: " + sys.version[:5] + "\nDiscord Version: " + discord.__version__)

threads = {"unitSetup": threading.Thread(target=botMentioned.unit.setup, args=(botMentioned.unit,))}
startThreads()
bot.run(token, reconnect=True)

asyncio.get_event_loop().close()
