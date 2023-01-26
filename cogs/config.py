#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
from discord.ext import commands
from discord.ui import View, Modal

from scripts.utils import BaseCog

class Config(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.prefixCommands = {
            "config": self.configPrefix,
        }
        
    @commands.slash_command(name="config", description="Configure JoeBot", 
        default_member_permissions=discord.Permissions(manage_guild=True))
    async def configSlash(self, ctx):
        view = CommandsSettingsView()
        await ctx.respond(embed=await view.newEmbed(), view=view, ephemeral=True)

    async def configPrefix(self, message):
        if message.guild is None:
            return await message.reply("This command can only be used in a server", mention_author=False)
        if not message.author.guild_permissions.manage_guild:
            return await message.add_reaction("🚫")
        view = CommandsSettingsView()
        await message.author.send(embed=await view.newEmbed(), view=view)

class CommandsSettingsView(View):
    async def newEmbed(self):
        embed = discord.Embed(
            title="Commands Settings",
            description="Configure JoeBot",
            color=Config.randomColor()
        )
        return embed

    @discord.ui.button(label="Change Prefix", style=discord.ButtonStyle.primary, emoji="❗")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(self.SetPrefixModal())

    class SetPrefixModal(Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(title="Change Prefix", *args, **kwargs)

            self.add_item(discord.ui.InputText(label="New Prefix", placeholder="!", max_length=1, required=False))

        async def callback(self, interaction):
            await interaction.response.edit_message(embed=await CommandsSettingsView.newEmbed(), view=CommandsSettingsView())


def setup(bot):
    bot.add_cog(Config(bot))
