#!/usr/bin/env python3
# JoeBot Copyright (C) 2021 JoeBlakeB
__author__ = "JoeBlakeB"
__copyright__ = "Copyright 2021, JoeBlakeB (joeblakeb.github.io)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import asyncio
import discord
import random
import re
import sys
import traceback

from emojis import emojis
from userJoinLeave import userJoinLeave
import keys

# Get Discord token

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

# Create bot

from modules import baseClass
class bot(baseClass.baseClass):
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    mentionedCommandsList = []
    for command in list(baseClass.baseClass.mentionedCommands):
        mentionedCommandsList += [re.compile(command)]
    exclamationCommandsList = []
    for command in list(baseClass.baseClass.exclamationCommands):
        exclamationCommandsList += [re.compile(command)]

    noCommandSpecified = ["wat?", "wat", "?", "the fuck you want?", emojis["HoodCate"], emojis["HoodCateHD"]]
    commandNotFoundList = ["what do you mean {0}", "I don't know what you mean by \"{0}\""]

    async def commandNotFound(self, message):
        if len(message.content.split(" ")) <= 2:
            await message.channel.send(random.choice(self.noCommandSpecified))
        else:
            await message.channel.send(random.choice(self.commandNotFoundList + self.noCommandSpecified).format(message.content))

    async def runCommand(message, command=None, messageContentLower="", generalCommands=False):
        if command == None:
            commandData = [bot.commandNotFound, ["message"], {"self":bot}]
        elif generalCommands:
            commandData = command[2:]
        else:
            mentioned = bool(messageContentLower.split(" ")[0] == "joebot")
            if mentioned:
                commandData = bot.mentionedCommands[command.pattern]
            else:
                commandData = bot.exclamationCommands[command.pattern]

        kwargs = commandData[2]
        for arg in commandData[1]:
            if arg == "message":
                kwargs[arg] = message
            elif arg == "messageContentLower":
                kwargs[arg] = messageContentLower
            elif arg == "commandContent":
                kwargs[arg] = messageContentLower[7-(6*int(not mentioned)):]
            elif arg == "bot":
                kwargs[arg] = bot
            elif arg == "typing":
                await message.channel.trigger_typing()

        try:
            await commandData[0](**kwargs)
        except discord.errors.Forbidden:
            pass
        except Exception:
            print(traceback.format_exc(), flush=True)
            await message.add_reaction("⚠️")

# Events

@bot.client.event
async def on_member_join(member):
    await userJoinLeave(member, True)

@bot.client.event
async def on_member_remove(member):
    await userJoinLeave(member, False)

@bot.client.event
async def on_ready():
    print("Logged in as {0.user}".format(bot.client), flush=True)

@bot.client.event
async def on_message(message):
    try:
        messageContentLower = message.content.lower()
        if messageContentLower.startswith(message.channel.guild.me.display_name.lower()):
            messageContentLower = "joebot" + messageContentLower[len(message.channel.guild.me.display_name):]
        if message.clean_content.startswith("@JoeBot"):
            messageContentLower = "joebot" + message.clean_content[7:].lower()
        if message.clean_content.startswith("@"+message.channel.guild.me.display_name):
            messageContentLower = "joebot" + message.clean_content[len(message.channel.guild.me.display_name)+1:].lower()

        # mentionedCommands & exclamationCommands
        if not message.author.bot and (messageContentLower.split(" ")[0] == "joebot" or
            (messageContentLower[0] == "!")):
            if messageContentLower.split(" ")[0] == "joebot":
                messageCommand = messageContentLower[7:]
                commandList = bot.mentionedCommandsList
            else:
                messageCommand = messageContentLower[1:]
                commandList = bot.exclamationCommandsList

            for command in commandList:
                if command.match(messageCommand):
                    await bot.runCommand(message, command, messageContentLower)
                    break
            else: # if no command found but joebot mentioned
                if messageContentLower.split(" ")[0] == "joebot":
                    message.content = messageContentLower[7:]
                    await bot.runCommand(message)
        # generalCommands
        else:
            for command in bot.generalCommands:
                if command[0] == "authorID":
                    if command[1] == message.author.id:
                        await bot.runCommand(message, command, messageContentLower, generalCommands=True)
                if command[0] == "authorDisplayNameRegex":
                    if command[1].match(message.author.display_name):
                        await bot.runCommand(message, command, messageContentLower, generalCommands=True)
    except IndexError: pass
    except discord.errors.Forbidden: pass
    except AttributeError as e:
        if str(e) != "'DMChannel' object has no attribute 'guild'":
            print(traceback.format_exc(), flush=True)
    except Exception:
        print(traceback.format_exc(), flush=True)

@bot.client.event
async def on_reaction_add(reaction, user):
    # if reaction.message.content in ["$wlt"] and reaction.message.author.id == 365154655313068032:
    #     await reaction.message.delete()
    if "> <https://redd.it/" in reaction.message.content and reaction.message.author.id == 796433833296658442 and reaction.emoji == "🔄":
        messageContent = str(reaction.message.content)
        await reaction.message.edit(content="<:hoodcate2:803666598526320690><a:teatime:834903558599213057>")
        await asyncio.sleep(5)
        await reaction.message.edit(content=messageContent)

# Start

print("Starting JoeBot with Python Version " + sys.version[:5] + " and Discord Version " + discord.__version__, flush=True)
eventLoop = asyncio.get_event_loop()
for task in bot.startTasks:
    if isinstance(task, list):
        eventLoop.create_task(task[0](bot))
    else:
        eventLoop.create_task(task)
bot.client.run(token, reconnect=True)

# Close

print("Closing", flush=True)
loop = asyncio.new_event_loop()
loop.run_until_complete(asyncio.wait(bot.closeTasks))
loop.close()
