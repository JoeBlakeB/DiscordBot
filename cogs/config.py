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
        view = CommandsSettingsView(self.bot.config[ctx.guild.id])
        await ctx.respond(embed=view.embed, view=view, ephemeral=True)

    async def configPrefix(self, message):
        if message.guild is None:
            return await message.reply("This command can only be used in a server", mention_author=False)
        if not message.author.guild_permissions.manage_guild:
            return await message.add_reaction("🚫")
        view = CommandsSettingsView(self.bot.config[message.guild.id])
        await message.author.send(embed=view.embed, view=view)


class CommandsSettingsView(View):
    def __init__(self, serverConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.serverConfig = serverConfig

        self.embed = discord.Embed(
            title="Commands Settings",
            color=Config.randomColor()
        )

        if serverConfig["messageCommandsEnabled"]:
            self.embed.add_field(
                name="Message Commands",
                value="```diff\n++  Enabled  ++\n```",
                inline=True
            )
            self.embed.add_field(
                name="Prefix",
                value="```\n " + serverConfig["prefix"] + " \n```",
                inline=True
            )
        else:
            self.embed.add_field(
                name="Message Commands",
                value="```diff\n--  Disabled  --\n```",
                inline=False
            )
            self.children[0].label = "Enable Message Commands"
            del self.children[1]

    @discord.ui.button(label="Disable Message Commands", style=discord.ButtonStyle.primary)
    async def toggleMessageCommands(self, button, interaction):
        self.serverConfig["messageCommandsEnabled"] ^= True
        view = CommandsSettingsView(self.serverConfig)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @discord.ui.button(label="Change Prefix", style=discord.ButtonStyle.primary, row=1)
    async def changePrefix(self, button, interaction):
        await interaction.response.send_modal(self.SetPrefixModal(self.serverConfig))

    class SetPrefixModal(Modal):
        def __init__(self, serverConfig, *args, **kwargs):
            super().__init__(title="Change Prefix", *args, **kwargs)
            self.serverConfig = serverConfig
            self.add_item(discord.ui.InputText(label="New Prefix", placeholder="!", max_length=1, required=False))

        async def callback(self, interaction):
            if self.children[0].value in (" ", "", None):
                prefix = "!"
            else:
                prefix = self.children[0].value
            self.serverConfig["prefix"] = prefix
            view = CommandsSettingsView(self.serverConfig)
            await interaction.response.edit_message(embed=view.embed, view=view)


def setup(bot):
    bot.add_cog(Config(bot))
