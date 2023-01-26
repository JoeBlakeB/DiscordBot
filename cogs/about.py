#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

from discord.ext import commands

from scripts.utils import BaseCog

class About(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.prefixCommands = {
            "ping": self.pingPrefix
        }

    ping = lambda self: f"Pong! {int(self.bot.latency * 1000)}ms"

    @commands.slash_command(name="ping", description="Ping!")
    async def pingSlash(self, ctx):
        await ctx.respond(self.ping(), ephemeral=True)

    async def pingPrefix(self, message):
        await message.reply(self.ping(), mention_author=False)


def setup(bot):
    bot.add_cog(About(bot))
