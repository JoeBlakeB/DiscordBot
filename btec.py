#!/usr/bin/env python3

import time
import threading
import discord

def setup():
    return
    if True: # if btec specs already setup
        try:
            btec.status = "200"
        except:
            time.sleep(1)
            btec.status = "200"
        return


    # import btecSetup

    try:
        pass
        # units = btecSetup.getUnitUrls()
    except Exception as e:
        btec.status = str(e)
        return
    print(units)
    btec.status = 404 #str(units)
    return
    #########################################
    if btec.terminate: return

    for unitURL in units:
        downloadUnit(unitURL)

class btec:
    terminate = False
    thread = threading.Thread(target = setup)
    thread.start()
    status = "200"
    # helpMessageShort = "short help btec"
    # helpMessageLong  = "LONG HELP btec"
    async def __new__(self, message, command):
        if self.status == "0":
            await message.channel.send("Waiting for BTEC specification download, " +
                "please try again in a few minutes")
        elif self.status[0] != "200":
            if len(self.status) == 3:
                await message.channel.send(":< pearson said HTTP error "+self.status)
            else:
                await message.channel.send("ÚwÙ something went wrong\n"+self.status)
        else:
            await message.channel.send("NOT IMPLEMENTED")

class unit:
    helpMessageShort = "short help unit"
    helpMessageLong  = "LONG HELP unit"
    units = {}
    async def __new__(self, message, command):
        if self.units == Exception:
            await message.channel.send("Cannot get unit specifications at the moment... please try later.")
            return
        try:
            unitNumber = int(command[2])
            embed = discord.Embed(title="Unit " + str(unitNumber) + " - " + list(self.units)[unitNumber - 1],
                url=self.units[list(self.units)[unitNumber-1]])
        except:
            try:
                searchv1 = " ".join(command[2:]).lower()
                searchv2 = ""
                searchCase = True
                for letter in searchv1:
                    if searchCase:
                        searchv2 += letter.upper()
                        searchCase = False
                    elif letter not in "abcdefghijklmnopqrstuvwxyz":
                        searchv2 += letter
                        searchCase = True
                    else:
                        searchv2 += letter

                embed = discord.Embed(title="Unit " + str(list(self.units).index(searchv2)+1) + " - " + searchv2,
                    url=self.units[searchv2])
            except Exception as e:
                await message.channel.send("I don't know what you want.")
                return
        await message.channel.send(embed=embed)

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
