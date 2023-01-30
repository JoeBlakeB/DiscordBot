#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
from discord.ext import commands

from scripts.utils import BaseCog, BaseSettingsView

class Config(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.prefixCommands = {
            "config": self.configPrefix,
        }
        self.configMenu = [
            StatusSettingsView,
            CommandsSettingsView
        ]
        
    @commands.slash_command(name="config", description="Configure JoeBot", 
        default_member_permissions=discord.Permissions(manage_guild=True))
    async def configSlash(self, ctx):
        view = StatusSettingsView(ctx.author, self.bot, self.bot.config[ctx.guild.id])
        await ctx.respond(embed=view.embed, view=view, ephemeral=True)

    async def configPrefix(self, message):
        if message.guild is None:
            return await message.reply("This command can only be used in a server", mention_author=False)
        if not message.author.guild_permissions.manage_guild:
            return await message.add_reaction("🚫")
        view = StatusSettingsView(message.author, self.bot, self.bot.config[message.guild.id])
        await message.author.send(embed=view.embed, view=view)


class StatusSettingsView(BaseSettingsView):
    priority = 0
    label = "Status"
    value = "status"
    emoji = "🤖"
    description = "View JoeBot's status"

    def __init__(self, author, *args, **kwargs):
        super().__init__(author, *args, **kwargs)

        self.embed = discord.Embed(
            title="JoeBot Settings",
            description="Change the settings for JoeBot.",
            color=BaseCog.randomColor(),
            fields=[
                discord.EmbedField(name="Ping", value=f"{int(self.bot.latency * 1000)}ms", inline=True),
                discord.EmbedField(name="Developer", value=f"<@{self.bot.ownerID}> [GitHub](https://github.com/JoeBlakeB/DiscordBot)", inline=True),
                discord.EmbedField(name="Uptime", value=f"<t:{self.bot.startTime}:R>", inline=True),
                discord.EmbedField(name="Version", value=f"{self.bot.version}", inline=True),
                discord.EmbedField(name="Servers", value=f"{len(self.bot.guilds)}", inline=True),
                discord.EmbedField(name="Commands", value=f"{len(self.bot.commands)}", inline=True)
            ]
        )

        self.embed.set_thumbnail(url=self.bot.user.avatar.url)


class CommandsSettingsView(BaseSettingsView):
    priority = 1
    label = "Commands"
    value = "commands"
    emoji = "❗"
    description = "Change the settings for using commands"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.embed = discord.Embed(
            title="Commands Settings",
            description="Change the settings for using JoeBot's commands.",
            color=Config.randomColor()
        )

        self.embed.set_thumbnail(url=self.bot.user.avatar.url)

        if self.serverConfig["messageCommandsEnabled"]:
            self.embed.add_field(
                name="Message Commands",
                value="```diff\n++  Enabled  ++\n```",
                inline=True
            )
            self.embed.add_field(
                name="Prefix",
                value="```\n " + self.serverConfig["prefix"] + " \n```",
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

    @discord.ui.button(label="Disable Message Commands", style=discord.ButtonStyle.primary, row=1)
    async def toggleMessageCommands(self, button, interaction):
        self.serverConfig["messageCommandsEnabled"] ^= True
        view = CommandsSettingsView(self.author, self.bot, self.serverConfig)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @discord.ui.button(label="Change Prefix", style=discord.ButtonStyle.primary, row=1)
    async def changePrefix(self, button, interaction):
        await interaction.response.send_modal(self.SetPrefixModal(self.author, self.bot, self.serverConfig))

    class SetPrefixModal(discord.ui.Modal):
        def __init__(self, *args):
            super().__init__(title="Change Prefix")
            self.args = args
            self.add_item(discord.ui.InputText(label="New Prefix", placeholder="!", max_length=1, required=False))

        async def callback(self, interaction):
            if self.children[0].value in (" ", "", None):
                prefix = "!"
            else:
                prefix = self.children[0].value
            self.args[2]["prefix"] = prefix
            view = CommandsSettingsView(*self.args)
            await interaction.response.edit_message(embed=view.embed, view=view)


def setup(bot):
    bot.add_cog(Config(bot))
