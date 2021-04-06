#!/usr/bin/env python3

import discord
import asyncio
import traceback
import sys
import time

import keys
from emojis import emojis

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
    for module in dir(modules):
        if not module[:2] == "__":
            module = getattr(modules, module)
            for moduleClass in dir(module):
                try:
                    mentionedCommands = getattr(module, moduleClass).mentionedCommands
#                    print(getattr(module, moduleClass).exclamationCommands)
                except AttributeError: pass

    mentionedCommandsList = list(mentionedCommands)
#    exclamationCommandsList = list(exclamationCommands)

    async def runCommand(message, command, exclamation=False):
        if exclamation:
            commandData = bot.exclamationCommands[command]
        else:
            commandData = bot.mentionedCommands[command]

        kwargs = commandData[2]
        for arg in commandData[1]:
            if arg == "message":
                kwargs[arg] = message

        await commandData[0](**kwargs)

# Events

@bot.client.event
async def on_member_join(member):
    pass # await userJoinLeave(member, True)

@bot.client.event
async def on_member_remove(member):
    pass # await userJoinLeave(member, False)

@bot.client.event
async def on_ready():
    print("Logged in as {0.user}".format(bot.client), flush=True)

@bot.client.event
async def on_message(message):
    try:
        messageContentLower = message.content.lower()
        if messageContentLower.startswith(message.channel.guild.me.display_name.lower()) and not message.author.bot:
            messageContentLower = "joebot" + messageContentLower[len(message.channel.guild.me.display_name):]

        if messageContentLower.split(" ")[0] == "joebot" and not message.author.bot:
            messageCommand = messageContentLower[7:]
            for command in bot.mentionedCommandsList:
                if command.split(" ") == 1:
                    if command == messageCommand.split(" ")[0]:
                        await bot.runCommand(message, command)
                else:
                    if messageCommand.startswith(command+" ") or messageCommand == command:
                        await bot.runCommand(message, command)
    except:
        await message.channel.send("<@365154655313068032> " + traceback.format_exc())

# Start

print("Starting JoeBot with Python Version " + sys.version[:5] + " and Discord Version " + discord.__version__, flush=True)
# asyncio.get_event_loop().create_task(thread)
bot.client.run(token, reconnect=True)

# Close

# print("Closing", flush=True)
# loop = asyncio.new_event_loop()
# loop.run_until_complete(asyncio.wait([botMentioned.reddit.prawInstance.close(), botMentioned.reddit.saveRecentSubmissions(botMentioned.reddit)]))
# loop.close()
