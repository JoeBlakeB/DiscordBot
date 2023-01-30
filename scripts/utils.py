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

    def __init__(self, author, bot, serverConfig, *args, **kwargs):
        """A menu for changing part of the bots settings in a server
        
        Parameters:
            author (discord.Member)
                The member who opened the menu
            bot (commands.Bot)
                The bot object
            serverConfig (ServerConfig)
                The config object for the server
        """
        super().__init__(*args, **kwargs)

        self.author = author
        self.bot = bot
        self.serverConfig = serverConfig

        select = discord.ui.Select(row=0,
            placeholder="Select a setting to view or change",
            options=bot.configMenuOptions
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction):
        """Callback for when a setting is selected"""
        view = self.bot.configMenuViews[interaction.data["values"][0]](self.author, self.bot, self.serverConfig)
        await interaction.response.edit_message(embed=view.embed, view=view)
