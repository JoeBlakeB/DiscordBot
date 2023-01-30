#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
import subprocess
import time
import warnings

from scripts.config import Config
from scripts.secrets import Secrets

class Bot(discord.Bot):
    botName = "JoeBot"
    ownerID = 365154655313068032
    prefixCommands = {}
    configMenu = []
    configMenuOptions = []
    configMenuViews = {}

    def __init__(self):
        self.config = Config()
        self.secrets = Secrets(self.config)
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        extensions = self.load_extensions("cogs")
        self.version = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode("utf-8").strip()
        self.startTime = int(time.time())

        for extension in extensions:
            if discord.errors.ExtensionFailed == type(extensions[extension]):
                warnings.warn(f"Extension {extension} failed to load:\n {extensions[extension]}")

        for cog in self.cogs:
            if hasattr(self.cogs[cog], "prefixCommands"):
                self.prefixCommands.update(self.cogs[cog].prefixCommands)
            if hasattr(self.cogs[cog], "configMenu"):
                self.configMenu += self.cogs[cog].configMenu

        self.configMenu.sort(key=lambda x: str(x.priority) + x.label)
        for selectOption in self.configMenu:
            self.configMenuOptions.append(discord.SelectOption(
                label=selectOption.label,
                value=selectOption.value,
                emoji=selectOption.emoji,
                description=selectOption.description))
            self.configMenuViews[selectOption.value] = selectOption
    
    def run(self):
        token = self.secrets.get("discord")
        if not token:
            raise ValueError("Please add your discord token to secrets.json")
        super().run(token)

    async def on_ready(self):
        print(f"Logged in as {self.user}", flush=True)
    
    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        if message.guild is not None and not self.config[message.guild.id, "messageCommandsEnabled"]:
            return

        msg = message.content.lower().strip()
        for prefix in ((
            self.user.display_name.lower(),
            "<@!" + str(self.user.id) + ">",
            "<@" + str(self.user.id) + ">") + 
            ((message.guild.me.display_name.lower(), self.config[message.guild.id, "prefix"]
                ) if hasattr(message.guild, "me") else ("!",))
        ):
            if msg.startswith(prefix):
                return await self.runPrefixCommand(msg[len(prefix):].strip(), message)
        if not hasattr(message.guild, "me"):
            return await self.runPrefixCommand(msg, message)
    
    async def runPrefixCommand(self, msg, message):
        for command in self.prefixCommands:
            if msg.startswith(command):
                return await self.prefixCommands[command](message)

if __name__ == "__main__":
    Bot().run()
