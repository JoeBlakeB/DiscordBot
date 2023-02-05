#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
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


class BaseSettingsView(discord.ui.View):
    embed = None
    priority = 10
    label = None
    value = None
    emoji = None
    description = None

    def __init__(self, author, bot, serverConfig, message=None, *args, **kwargs):
        """A menu for changing part of the bots settings in a server
        
        Parameters:
            author (discord.Member)
                The member who opened the menu
            bot (commands.Bot)
                The bot object
            serverConfig (ServerConfig)
                The config object for the server
        """
        bot.activeViews.append(self)
        super().__init__(*args, **kwargs, timeout=300)

        self.author = author
        self.bot = bot
        self.serverConfig = serverConfig

        if message:
            self.message = message

        select = discord.ui.Select(row=0,
            placeholder="Select a setting to view or change",
            options=bot.configMenuOptions
        )
        select.callback = self.selectCallback
        self.add_item(select)

    def create(self):
        """Create an embed about the config and customize the buttons"""
        self.embed = discord.Embed(
            title="JoeBot Config",
            color=BaseCog.randomColor()
        )

    async def selectCallback(self, interaction):
        """Callback for when a setting is selected"""
        self.bot.activeViews.remove(self)
        view = self.bot.configMenuViews[interaction.data["values"][0]](self.author, self.bot, self.serverConfig, message=self.message)
        await interaction.response.edit_message(embed=view.embed, view=view)
        self.stop()

    async def on_timeout(self):
        """Disable the menu when it times out"""
        self.bot.activeViews.remove(self)
        self.disable_all_items()
        self.embed.set_footer(text="Menu timed out, run the command again to continue.")
        await self.message.edit(view=self, embed=self.embed)

    async def refreshEmbed(self, interaction):
        """Refresh the menu with a new view
        
        Parameters:
            interaction (discord.Interaction)
                The interaction that triggered the refresh
        """
        self.create()
        await interaction.response.edit_message(view=self, embed=self.embed)
