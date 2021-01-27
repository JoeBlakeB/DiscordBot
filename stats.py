import discord
import sys
import os
import subprocess
import platform
import time
import datetime
try:
    import psutil
except: pass

class stats:
    help = {"list": True, "ListPriority": 2, "Title":"Stats",
        "ShortHelp": "Get bot stats. *@{displayName} stats*",
        "LongHelp": "Gives stats for {displayName}.\n"+
        "Use **@{displayName} stats** to view bot stats."}

    uptime = {"Connected":False, "Script Start":0, "Total Uptime":0, "Connection Start": 0, "Connection Uptime":0, "Uptime Percent":0}

    def updateUptime(self):
        if self.uptime["Script Start"] == 0:
            self.uptime["Script Start"] = time.time()
        if self.uptime["Connected"] and self.uptime["Connection Start"] == 0:
            self.uptime["Connection Start"] = time.time()

        if not self.uptime["Connected"]:
            self.uptime["Total Uptime"] += self.uptime["Connection Uptime"]
            self.uptime["Connection Uptime"] = 0
            self.uptime["Connection Start"] = 0
        else:
            self.uptime["Connection Uptime"] = time.time() - self.uptime["Connection Start"]

        try:                                      #                  True Total Uptime                  #            #  Max uptime possible since start  #
            self.uptime["Uptime Percent"] =  (self.uptime["Total Uptime"] + self.uptime["Connection Uptime"]) / (time.time() - self.uptime["Script Start"])
        except ZeroDivisionError:
            self.uptime["Uptime Percent"] = 0

    def convertToDays(seconds):
        timeSegments = [int(seconds), 0, 0, 0]

        for i in range(3):
            if timeSegments[i] // [60, 60, 24][i] != 0:
                timeSegments[i+1] = timeSegments[i] // [60, 60, 24][i]
                timeSegments[i] %= [60, 60, 24][i]

        returnTime = ""
        for i in range(4):
            if timeSegments[i] != 0:
                returnTime = str(timeSegments[i]) + "smhd"[i] + " " + returnTime

        return returnTime

    def version():
        try:
            amountOfCommits = subprocess.check_output("git rev-list --count HEAD", shell=True, stderr=subprocess.STDOUT)
            return "\nJoeBot Version: " + str(amountOfCommits, "utf-8")
        except subprocess.CalledProcessError:
            return ""

    async def __new__(self, message, command, parentClass):
        embed = discord.Embed()
        embed.color = parentClass.__embedColor__()
        bot = parentClass.__bot__()

        embed.title = "JoeBot Stats"
        embed.description = "Python Version: " + sys.version[:5] + "\nDiscord Version: " + discord.__version__
        embed.description += self.version()
        embed.description += "Server Count: " + str(len(bot.guilds))
        try:
            process = psutil.Process(os.getpid())
            memory = "\nMemory Usage: " + str(int(process.memory_info().rss / (1024 ** 2))) + "MB"
            cpu = "\nCPU Usage: " + str(process.cpu_percent(interval=None)) + "%"
            embed.description += cpu + memory
        except NameError: pass
        embed.description += "\nOS: " + platform.system() + " " + platform.release()
        embed.description += "\nPing: " + str(int(bot.latency*1000)) + "ms"

        self.updateUptime(self)
        embed.description += "\nTotal Uptime: " + self.convertToDays(self.uptime["Total Uptime"] + self.uptime["Connection Uptime"])
        embed.description += "\nConnection Uptime: " + self.convertToDays(self.uptime["Connection Uptime"])
        embed.description += "\nUptime Percentage: " + str(int(round(self.uptime["Uptime Percent"]*100, 0))) + "%"

        await message.channel.send(embed=embed)
