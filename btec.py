#!/usr/bin/env python3

import threading
import discord

class unit:
    units = {}
    help = {"list": True, "ListPriority": 2, "Title":"Unit",
        "ShortHelp": "View unit specification.",
        "LongHelp": "View unit specification.\n"+
        "*@{displayName} Unit <number>* Get a link to the unit specification.\n"+
        "Work in progress:"+
        "\n*@{displayName} Unit <number>* View unit summary."+
        "\n*@{displayName} Unit <number> Assignment <number>* View specific assignment."
        "\n*@{displayName} Unit <number> <grade>* View specific grade. e.g. P#, M#, D#"
        "\n*@{displayName} Unit <name>* View unit by name."}
    async def __new__(self, message, command, parentClass):
        if self.units == Exception:
            await message.channel.send("Cannot get unit specifications at the moment... please try later.")
            return

        # Try to get unit number
        try:
            unitNumber = int(command[2])
            if unitNumber <= 0 or unitNumber > len(self.units):
                # if unit number is out of range, tell the user & return
                await message.channel.send("I dont think Unit {0} exists".format(unitNumber))
                return
        except:
            unitNumber = 0
        if unitNumber == 0:
            unitNumber, subCommand = self.search(command[2:])
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

        await message.channel.send(embed=embed)

    def search(command):
        raise NotImplementedError("NotImplementedError: Get unit by name is still work in progress")

    def setup(self):
        try:
            with open("btecURLs.txt") as urlFile:
                units = urlFile.read().strip().split()
            for unit in units:
                self.units[unit[115:-4].replace("-", " ").strip()] = unit
        except:
            self.units = Exception

unitSetup = threading.Thread(target = unit.setup, args = (unit,))
unitSetup.start()
