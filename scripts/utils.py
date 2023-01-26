#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

from discord.ext import commands
import random

class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def randomColor():
        """Returns a random color
        TODO: use HSV to get a random color that looks good"""
        return random.randint(0, 0xFFFFFF)
