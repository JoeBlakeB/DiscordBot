import discord

class help:
    help = {"list": True, "ListPriority": 1, "Title":"Help",
        "ShortHelp": "Get help for commands. *@{displayName} help <command>* for detailed info.",
        "LongHelp": "Gives help on using {displayName}.\n"+
        "*@{displayName} help <number>* to view command list page.\n"+
        "*@{displayName} help <command>* for detailed info on a command."}
    commandList = []
    commandsPerPage = 6
    async def __new__(self, message, command, parentClass):
        # List of commands
        if self.commandList == []:
            for commandClass in dir(parentClass):
                if "__" not in commandClass:
                    try:
                        if getattr(parentClass, commandClass).help["list"] == True:
                            self.commandList += [commandClass]
                    except: pass

            # Sort commandList by ListPriority
            ## TODO

        # Try to get what command user wants help for / help page number
        try:
            if command[2] in dir(parentClass) and "__" not in command[2]:
                helpForCommand = getattr(parentClass, command[2]).help
                if helpForCommand["LongHelp"]: pass
            else:
                helpForCommand = {"LongHelp":False}
        except:
            helpForCommand = {"LongHelp":False}
        try:
            helpPage = int(command[2])
            if helpPage <= 0 or helpPage >= (len(self.commandList)/commandsPerPage)+1:
                helpPage = 1
        except:
            helpPage = 1

        embed = discord.Embed()
        embed.color = parentClass.__embedColor__()
        # Give help for a command
        if helpForCommand["LongHelp"]:
            embed.title = message.channel.guild.me.display_name + " " + helpForCommand["Title"]
            embed.description = (helpForCommand["LongHelp"]
                .format(displayName = message.channel.guild.me.display_name))

        # Give page of available commands
        else:
            embed.title = message.channel.guild.me.display_name + " Help"
            embed.description = ""
            listOffset = (helpPage-1)*self.commandsPerPage

            for command in self.commandList[0+(listOffset):6+(listOffset)]:
                command = getattr(parentClass, command).help
                embed.description += ("\n**" + command["Title"] +
                    "**\n> " + command["ShortHelp"]
                    .format(displayName = message.channel.guild.me.display_name))
            embed.description = embed.description[1:]
            # Tell user about multiple pages
            if (len(self.commandList)/self.commandsPerPage)+1 > 2:
                pageNumber = (str(helpPage) + "/" +
                str(int(((len(self.commandList)-1)/self.commandsPerPage)+1)))
                embed.title += (" (page " + pageNumber +")")
                embed.description += "\nPage "+ pageNumber +(" - @{displayName} help #"
                    .format(displayName = message.channel.guild.me.display_name))

        await message.channel.send(embed=embed)
