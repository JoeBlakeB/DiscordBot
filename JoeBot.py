#!/usr/bin/env python3

import discord
import os
import re

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
    # Ignore own messages
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if re.match(r"<:(xander|fido):[0-9]+>", message.content.lower()):
        await message.add_reaction(message.content[1:-1])

bot.run(token)
