#!/usr/bin/env python3

import discord

class unit:
    help = {"list": True, "ListPriority": 3, "Title":"Unit",
        "ShortHelp": "View unit specification.",
        "LongHelp": "View unit specification.\n"+
        "**@{displayName} Unit <number>** Get a link to the unit specification.\n"+
        "\nWork in progress:"+
        "\n**@{displayName} Unit <number>** View unit summary."+
        "\n**@{displayName} Unit <number> Learning Outcome <number>** View specific learning outcome."+
        "\n**@{displayName} Unit <number> Assignment <number>** View specific assignment."+
        "\n**@{displayName} Unit <number> <grade>** View specific grading criteria. e.g. P#, M#, D#"+
        "\n**@{displayName} Unit <name>** View unit by name."+
        "\n**@{displayName} Unit Search <name>** Search for units."}
    units = {}
    async def __new__(self, message, command, parentClass):
        if self.units == Exception:
            await message.channel.send("Cannot get unit specifications at the moment... please try later.")
            return

        if len(command) >= 3:
            if command[2].lower() == "search":
                self.search(self, message, command, parentClass)
                return

        # Try to get unit number
        try:
            unitNumber = int(command[2])
            if unitNumber <= 0 or unitNumber > len(self.units):
                # if unit number is out of range, tell the user & return
                await message.channel.send("I dont think Unit {0} exists.".format(unitNumber))
                return
        except:
            unitNumber = 0
        if unitNumber == 0:
            unitNumber, subCommand = self.getUnitByName(self, command[2:])
            # if unitNumber is still 0, tell user cannot find unit
            if unitNumber == 0:
                await message.channel.send("Could not find that Unit. "+
                    "Check for typos or specify Unit number instead."+
                    " This is currently work in progress so expect some bugs.")
                return
        else:
            subCommand = command[3:]

        embed = discord.Embed()
        embed.title = "Unit " + str(unitNumber) + " - " + list(self.units)[unitNumber - 1]
        embed.color = parentClass.__embedColor__()
        embed.url=self.units[list(self.units)[unitNumber-1]]

        if len(subCommand) >= 1:
            if subCommand[0].lower() in ["assignment", "pass", "merit", "distinction", "learning", "outcome", "objective",
                                        "a", "p", "m", "d", "lo", "l", "o"]:
                if len(subCommand) == 1:
                    description = ["summary", "You need to specify the {0} you want.".format(subCommand[0])]
                elif " ".join(subCommand[0:1]).lower() in ["learning outcome", "learning objective", "lo"] and len(subCommand) >= 3:
                    try:
                        description = ["l", int(subCommand[2])]
                    except ValueError:
                        description = ["summary", "{0} isnt a number.".format(subCommand[2])]
                else:
                    try:
                        description = [subCommand[0].lower()[0], int(subCommand[1])]
                    except ValueError:
                        description = ["summary", "{0} isnt a number.".format(subCommand[1])]
            elif len(subCommand[0]) == 2 and subCommand[0].lower()[0] in "apmdlo" and subCommand[0][1] in "123456789":
                description = [subCommand[0].lower()[0], int(subCommand[0][1])]
            elif len(subCommand[0]) == 3 and subCommand[0].lower()[0:1] == "lo" and subCommand[0][2] in "123456789":
                description = ["l", int(subCommand[0][2])]
            else:
                description = ["summary", "I don't know what you mean by {0}.".format(" ".join(subCommand))]
        else:
            description = ["summary", False]

        if description[0] == "summary":
            embed.description = "Viewing unit summary is work in progress"

        elif description[0] in ["l", "o"]: # Learning Outcome
            embed.description = "Viewing specific learning outcome is work in progress"

        elif description[0] == "a": # Assignment
            embed.description = "Viewing specific assignment is work in progress"

        elif description[0] in ["p", "m", "d"]: # Grading Criteria
            embed.description = "Viewing specific grading criteria is work in progress"

        await parentClass.__long_send__(message, embed=embed)

    def getUnitByName(self, command):
        raise NotImplementedError("NotImplementedError: getUnitByName is still work in progress")
        # return unitNumber, subCommand

    def search(self, message, command, parentClass):
        raise NotImplementedError("NotImplementedError: search still work in progress")

    def setup(self):
        try:
            with open("btecURLs.txt") as urlFile:
                units = urlFile.read().strip().split()
            for unit in units:
                self.units[unit[115:-4].replace("-", " ").strip()] = unit
        except:
            self.units = Exception
