#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
from discord.ext import commands
import sys

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

        self.createEmbed()

        if self.bot.ownerID == author.id:
            self.ownerConfig()

    def createEmbed(self):
        """Create an embed with the basic bot info"""
        self.embed = discord.Embed(
            title="JoeBot Settings",
            description="Select an option from the dropdown menu to change the settings for JoeBot.",
            color=BaseCog.randomColor(),
            fields=[
                discord.EmbedField(name="Ping", value=f"{int(self.bot.latency * 1000)}ms", inline=True),
                discord.EmbedField(name="Servers", value=len(self.bot.guilds), inline=True),
                discord.EmbedField(name="Commands", value=len(self.bot.commands), inline=True),
                discord.EmbedField(name="Version", value=self.bot.version, inline=True),
                discord.EmbedField(name="Uptime", value=f"<t:{self.bot.startTime}:R>", inline=True),
                discord.EmbedField(name="Developer", value=f"<@{self.bot.ownerID}> [GitHub](https://github.com/JoeBlakeB/DiscordBot)", inline=True),
            ]
        )

        self.embed.set_thumbnail(url=self.bot.user.avatar.url)

    def ownerConfig(self):
        """Add the owner config options to the embed
        
        TODO: update, and restart buttons"""

        status = self.getStatusString()
        if status:
            self.embed.add_field(name="Status", value=status, inline=False)

        self.embed.add_field(
            name="Python Version", value=sys.version.split(" ")[0], inline=True)
        self.embed.add_field(
            name="Pycord Version", value=discord.__version__, inline=True)

        availableVersion = "TODO"# self.bot.getVersion()

        if availableVersion != self.bot.version:
            self.embed.add_field(name="JoeBot Version Available", value=availableVersion, inline=False)

        statusSelect = discord.ui.Select(row=1,
            placeholder={
                "online": "🟢 Online",
                "idle": "🟡 Idle",
                "dnd": "🔴 Do Not Disturb",
                "invisible": "⚪ Invisible"
            }[self.bot.botConfig["presence", "status"]],
            options=[
                discord.SelectOption(label="Online", value="online", emoji="🟢"),
                discord.SelectOption(label="Idle", value="idle", emoji="🟡"),
                discord.SelectOption(label="Do Not Disturb", value="dnd", emoji="🔴"),
                discord.SelectOption(label="Invisible", value="invisible", emoji="⚪")
            ]
        )
        statusSelect.callback = self.statusSelectCallback
        self.add_item(statusSelect)

        activityButton = discord.ui.Button(label="Set Activity", style=discord.ButtonStyle.primary, row=2)
        activityButton.callback = self.setActivityCallback
        self.add_item(activityButton)

    def getStatusString(self):
        activity = self.bot.botConfig["presence", "activity"]
        if activity:
            activityType = {
                0: "Playing",
                1: "Streaming",
                2: "Listening to",
                3: "Watching",
                5: "Competing in"
            }[activity[0]]
            if activity[2]:
                return f" {activityType} [{activity[1]}]({activity[2]})"
            else:
                return f" {activityType} {activity[1]}"

    async def statusSelectCallback(self, interaction):
        self.bot.botConfig["presence", "status"] = interaction.data["values"][0]
        await self.bot.changePresence()
        view = StatusSettingsView(interaction.user, self.bot, self.serverConfig)
        await interaction.response.edit_message(embed=view.embed, view=view)

    async def setActivityCallback(self, interaction):
        await interaction.response.send_modal(self.SetActivityModal(self.author, self.bot, self.serverConfig))
    
    class SetActivityModal(discord.ui.Modal):
        def __init__(self, *args):
            super().__init__(title="Set Prefix")
            self.args = args
            self.bot = args[1]
            self.add_item(discord.ui.InputText(label="Type", value="Playing",
                placeholder="Playing, Streaming, Watching, Listening, Competing"))
            self.add_item(discord.ui.InputText(label="Name", required=False,
                placeholder="The name of the activity"))
            self.add_item(discord.ui.InputText(label="URL (For Streaming only)", required=False,
                placeholder="The URL of the stream"))

        async def callback(self, interaction):
            if self.children[1].value:
                try:
                    activityType = {"P": 0, "S": 1, "L": 2, "W": 3, "C": 5}[self.children[0].value[0].upper()]
                except KeyError:
                    activityType = 0
                activityName = self.children[1].value
                activityURL = self.children[2].value if activityType == 1 else None
                self.bot.botConfig["presence", "activity"] = [activityType, activityName, activityURL]
            else:
                self.bot.botConfig["presence", "activity"] = None
            await self.bot.changePresence()
            view = StatusSettingsView(*self.args)
            await interaction.response.edit_message(embed=view.embed, view=view)


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
