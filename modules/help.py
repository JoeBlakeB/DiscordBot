import discord
import re

import baseClass

try:
    import psutil
except ImportError:
    psutil = False

class help(baseClass.baseClass):
    defaultHelpMessage = {"title":"JoeBot Help", "description":"Developer: <@365154655313068032> [(GitHub)](https://github.com/JoeBlakeB/DiscordBot)\n\nTo use JoeBot, say:\n**<@796433833296658442> <command>**\nor **joebot <command>**\nor **!<command>**\nor in direct messages with just the command", "thumbnail":"https://cdn.discordapp.com/avatars/796433833296658442/45d01f0b2d42a5e23e552b75f359525e.png"}
    helpRegex = False
    async def helpCommand(message, messageContentLower, bot):
        if not help.helpRegex:
            help.compileRegex()

        if messageContentLower[0] == "!":
            exclamation = True
            messageContentLower = messageContentLower[6:]
        else:
            exclamation = False
            messageContentLower = messageContentLower[12:]

        if messageContentLower == "":
            return await help.embed(message, help.defaultHelpMessage, await help.jmusicplayerInfo())

        for command in help.helpRegex:
            if command.match(messageContentLower):
                if "embed" in help.helpRegex[command][0]:
                    return await help.embed(message, help.helpRegex[command][1])
                elif "plaintext" in help.helpRegex[command][0]:
                    return await message.channel.send(help.helpRegex[command][1])
        else:
            if not exclamation:
                await help.embed(message, help.defaultHelpMessage, await help.jmusicplayerInfo())

    async def embed(message, embedContent, descriptionExtra = ""):
        embed = discord.Embed()
        embed.title = embedContent["title"]
        embed.description = embedContent["description"] + descriptionExtra
        if "thumbnail" in embedContent:
            embed.set_thumbnail(url=embedContent["thumbnail"])
        await message.channel.send(embed=embed)

    def compileRegex():
        help.helpRegex = {}
        availableCommands = []
        for command in help.help:
            help.helpRegex[re.compile(command)] = help.help[command]
            if "include" in help.help[command][0]:
                availableCommands.append(command)

        if len(availableCommands) != 0:
            help.defaultHelpMessage["description"] += "\n\nAvailable Commands:\n" + ", ".join(availableCommands) + "\n\nUse **<@796433833296658442> help <command>** for more information."

    async def jmusicplayerInfo():
        if psutil:
            for proc in psutil.process_iter():
                if len(proc.cmdline()) == 4:
                    print(proc.cmdline(), flush=True)
                    if proc.cmdline()[:-1] == ["/usr/bin/java", "-Dnogui=true", "-jar"] and "JMusicBot" in proc.cmdline()[-1]:
                        return "\n\n[JMusicBot](https://github.com/jagrosh/MusicBot) is currently running on JoeBot, use !musichelp for help music commands."
        return ""


help.mentionedCommands["help(?!\S)"] = [help.helpCommand, ["message", "messageContentLower", "bot"], {}]
help.exclamationCommands["help(?!\S)"] = [help.helpCommand, ["message", "messageContentLower", "bot"], {}]
