#!/usr/bin/env python3

import random

class good:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() == "bot":
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception
class bad:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() == "bot":
            await message.channel.send(random.choice(["ÓnÒ why am I a bad bot?", "ÒwÓ no you", "thats mean"]))
        else:
            raise Exception
