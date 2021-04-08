#!/usr/bin/env python3

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

class bot:
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    import modules
    mentionedCommands = {}
    exclamationCommands = {}
    startTasks = []
    closeTasks = []
    for module in dir(modules):
        if not module[:2] == "__":
            module = getattr(modules, module)
            for moduleClass in dir(module):
                try:
                    moduleClass = getattr(module, moduleClass)
                    startTasks += moduleClass.startTasks
                    closeTasks += moduleClass.closeTasks
                    for command in moduleClass.mentionedCommands:
                        mentionedCommands[re.compile(command)] = moduleClass.mentionedCommands[command]
                    for command in moduleClass.exclamationCommands:
                        exclamationCommands[re.compile(command)] = moduleClass.exclamationCommands[command]
                except AttributeError: pass

    mentionedCommandsList = list(mentionedCommands)
    exclamationCommandsList = list(exclamationCommands)

    noCommandSpecified = ["wat?", "wat", "?", "the fuck you want?", emojis["HoodCate"], emojis["HoodCateHD"]]
    commandNotFoundList = ["what do you mean {0}", "I don't know what you mean by \"{0}\""]

    async def commandNotFound(self, message):
        if len(message.content.split()) <= 2:
            await message.channel.send(random.choice(self.noCommandSpecified))
        else:
            await message.channel.send(random.choice(self.commandNotFoundList + self.noCommandSpecified).format(message))

    async def runCommand(message, command=None, messageContentLower=""):
        if command == None:
            commandData = [bot.commandNotFound, ["message"], {"self":bot}]
        elif bool(messageContentLower.split(" ")[0] == "joebot"):
            commandData = bot.mentionedCommands[command]
        else:
            commandData = bot.exclamationCommands[command]

        kwargs = commandData[2]
        for arg in commandData[1]:
            if arg == "message":
                kwargs[arg] = message
            elif arg == "messageContentLower":
                kwargs[arg] = messageContentLower
            elif arg == "typing":
                await message.channel.trigger_typing()

        try:
            await commandData[0](**kwargs)
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
    bot.modules.status.status.bot = bot

@bot.client.event
async def on_message(message):
    try:
        if message.author.bot: return
        messageContentLower = message.content.lower()
        if messageContentLower.startswith(message.channel.guild.me.display_name.lower()):
            messageContentLower = "joebot" + messageContentLower[len(message.channel.guild.me.display_name):]
        if message.clean_content.startswith("@JoeBot"):
            messageContentLower = "joebot" + message.clean_content[7:].lower()
        if message.clean_content.startswith("@"+message.channel.guild.me.display_name):
            messageContentLower = "joebot" + message.clean_content[len(message.channel.guild.me.display_name)+1:].lower()

        if messageContentLower.split(" ")[0] == "joebot" or messageContentLower[0] == "!":
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
    except IndexError: pass
    except Exception:
        print(traceback.format_exc(), flush=True)

# Start

print("Starting JoeBot with Python Version " + sys.version[:5] + " and Discord Version " + discord.__version__, flush=True)
eventLoop = asyncio.get_event_loop()
for task in bot.startTasks:
    eventLoop.create_task(task)
bot.client.run(token, reconnect=True)

# Close

print("Closing", flush=True)
loop = asyncio.new_event_loop()
loop.run_until_complete(asyncio.wait(bot.closeTasks))
loop.close()
