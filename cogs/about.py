#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixCommands = {
            "ping": self.pingPrefix
        }

    pingBase = lambda self: f"Pong! {int(self.bot.latency * 1000)}ms"

    @commands.slash_command(description="Ping!")
    async def ping(self, ctx):
        await ctx.respond(self.pingBase(), ephemeral=True)

    async def pingPrefix(self, message):
        await message.channel.send(self.pingBase())


def setup(bot):
    bot.add_cog(About(bot))
