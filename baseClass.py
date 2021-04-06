import emojis
import random

class baseClass:
    mentionedCommands = {}
    exclamationCommands = {}

    async def __new__(self, message, text):
        await message.channel.send(text)
