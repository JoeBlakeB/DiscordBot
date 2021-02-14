#!/usr/bin/env python3

import discord
import os
import sys
import re
import random
import datetime
import threading
import asyncio

import keys

try:
    token = keys.read("Discord")
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
            dogeValue = round(botMentioned.crypto.getValue("doge") * 100, 2)
            if dogeValue == 0:
                now = datetime.datetime.now()
                timeNow = int(str(now.hour)+("0"+str(now.minute))[-2:])
                if now.weekday() in [0, 2, 4] and timeNow >= 845 and timeNow <= 1600:
                    await bot.change_presence(activity=discord.Activity(name="@JoeBot help", type=2))
                else:
                    await bot.change_presence(activity=discord.Activity(name=random.choice(songs), type=2))
            else:
                await bot.change_presence(activity=discord.Activity(name="doge @ "+str(dogeValue)+"p 🚀🌑", type=3))
            await asyncio.sleep(random.randint(200, 300))
        except:
            botPresenceRunning = False
            return

joinMessages = ["I should probably warn you that {name} is a registered sex offender."]
leaveMessages = ["{name} leaving is kinda poggers."]

async def userJoinLeave(member, messageList):
    for channelName in ["welcome", "general"]:
        channel = discord.utils.get(member.guild.text_channels, name=channelName)
        if channel != None:
            try:
                await channel.send(random.choice(messageList).format(name=member.display_name))
                return
            except: pass

@bot.event
async def on_member_join(member):
    await userJoinLeave(member, joinMessages)

@bot.event
async def on_member_remove(member):
    await userJoinLeave(member, leaveMessages)


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

    try: botNames = ["joebot", message.channel.guild.me.display_name.lower()]
    except: botNames = "joebot"

    if re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])

    elif "kev" in message.content.lower():
        emoji = discord.utils.get(message.channel.guild.emojis, name='xander')
        await message.add_reaction(emoji)

    if message.content.lower() == "git gud":
        await message.channel.send("git: 'gud' is not a git command.")

    elif message.content.startswith("<@!"+str(bot.user.id)+">") or message.content.startswith("<@"+str(bot.user.id)+">") or (message.content.split(" ")[0].lower() in botNames):
        await botMentioned(message)

    else:
        for i in message.content.split():
            if i in ["69", "420"]:
                await message.channel.send("Nice.")
                break
            elif i.lower() in ["pogchamp", "poggers", "pogger", "pogging", "pog"]:
                await message.channel.send(random.choice(["Pog", "Poggers", "Pogger", "PogChamp", "Pogging", "This is poggers", "This is very poggers"]))
                break

class botMentioned:
    from help import help
    from btec import unit
    from stuff import good, bad, hi, hey, hello, say, gun, kill, pogchamp, porn
    from stats import stats
    from crypto import crypto
    from reddit import reddit

    async def __new__(self, message):
        command = message.content.strip()
        while "__" in command: command = command.replace("__", "")
        while "  " in command: command = command.replace("  ", " ")
        command = command.split()

        if command[1][:2] == "r/":
            command[1:2] = ["reddit", command[1][2:]]

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
