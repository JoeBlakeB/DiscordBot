#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import discord
import subprocess
import time
import warnings

import scripts.config
import scripts.secrets

class Bot(discord.Bot):
    botName = "JoeBot"
    ownerID = 365154655313068032
    prefixCommands = {}
    configMenu = []
    configMenuOptions = []
    configMenuViews = {}

    def __init__(self):
        self.config = scripts.config.Config()
        self.secrets = scripts.secrets.Secrets(self.config)
        self.botConfig = scripts.config.ConfigCustomDefaults({
            "status": "online",
            "activity": None
        })

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        extensions = self.load_extensions("cogs", recursive=True, store=True)
        self.version = self.getVersion()
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
        await self.changePresence()

    async def changePresence(self):
        """Sets the bot's presence according to the config file."""
        activity = self.botConfig["presence", "activity"]
        if activity:
            activity = discord.Activity(
                type=discord.ActivityType(activity[0]),
                name=activity[1],
                url=activity[2])
        await self.change_presence(activity=activity,
            status=discord.Status(self.botConfig["presence", "status"]))
    
    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return
        if message.guild and not self.config[message.guild.id, "messageCommandsEnabled"]:
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

    @staticmethod
    def getVersion():
        return subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode("utf-8").strip()

if __name__ == "__main__":
    Bot().run()
