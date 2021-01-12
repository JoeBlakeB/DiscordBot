#!/usr/bin/env python3

import random

class good:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() == "bot":
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception
