import asyncio
import discord
import random
import requests
import time
import datetime
import sys
import subprocess
import platform
import os
import traceback
try:
    import psutil
except: pass

import baseClass
import modules.crypto

songs = ["Cat", "Dog", "Door", "Living Mice", "Mice on Venus", "Moog City", "Subwoofer Lullaby", "Équinoxe",
         "Aria Math", "Blind Spots", "Blocks", "Chirp", "Dreiton", "Strad", "Taswell", "Wait", "Ward"]

class status(baseClass.baseClass):
    bot = None
    async def presence(bot):
        status.bot = bot
        await asyncio.sleep(10)
        while True:
            try:
                try:
                    mcServer = subprocess.check_output(["nmap", "-p", "25565", "localhost"]).decode("utf-8")
                except:
                    mcServer = "closed"
                if "open" in mcServer:
                    await status.bot.client.change_presence(activity=discord.Game(name="MC @ " + requests.get("https://ipinfo.io/ip").text))
                    sleepTill = time.time() + 200
                else:
                    dogeValue = round(modules.crypto.crypto.getValue("dogecoin") * 100, 2)
                    if dogeValue > 10: dogeValue = round(dogeValue, 1)
                    if dogeValue > 100: dogeValue = int(dogeValue)
                    if dogeValue == 0:
                        await status.bot.client.change_presence(activity=discord.Activity(name="C418 - "+random.choice(songs), type=2))
                        sleepTill = time.time() + random.randint(200, 400)
                    else:
                        await status.bot.client.change_presence(activity=discord.Activity(name="DOGE @"+str(dogeValue)+"p 🚀🌑", type=3))
                        sleepTill = time.time() + 600
                while True:
                    await asyncio.sleep(20)
                    if sleepTill < time.time():
                        break
            except Exception:
                print(traceback.format_exc())
                await asyncio.sleep(120)

    async def ping(message):
        pong = "Pong!"
        try:
            pong += " " +  str(int(status.bot.client.latency*1000)) + "ms"
        except Exception: pass
        await message.channel.send(pong)

    def version():
        try:
            amountOfCommits = subprocess.check_output("git rev-list --count HEAD", shell=True, stderr=subprocess.STDOUT)
            return "\nJoeBot Version: " + str(amountOfCommits, "utf-8")
        except subprocess.CalledProcessError:
            return "\n"

    async def status(self, message):
        embed = discord.Embed()
        embed.title = "JoeBot"
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796434329831604288/851087338662658068/DiscordBot_-_2021-02-17_-_Amogus_2.png")
        embed.description = "Developer: <@365154655313068032>\n"
        embed.description += "[GitHub](https://github.com/JoeBlakeB/DiscordBot)\n"
        embed.description += "[Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=796433833296658442&permissions=117824&scope=bot)\n"
        embed.description += "Python Version: " + sys.version[:5] + "\nDiscord Version: " + discord.__version__
        embed.description += self.version()
        try:
            embed.description += "Server Count: " + str(len(status.bot.client.guilds))
            embed.description += "\nPing: " + str(int(status.bot.client.latency*1000)) + "ms\n"
        except Exception: pass

        try:
            process = psutil.Process(os.getpid())
            memory = "Memory Usage: " + str(int(process.memory_info().rss / (1024 ** 2))) + "MB\n"
            # cpu = "CPU Usage: " + str(process.cpu_percent(interval=None)) + "%\n"
            embed.description += memory
        except NameError: pass

        try:
            embed.description += "OS: " + str(subprocess.check_output(["lsb_release","-is"]), "utf-8").strip() + " " + platform.system()
        except:
            embed.description += "OS: " + platform.system() + " " + platform.release()

        await message.channel.send(embed=embed)

    async def neofetch(self, message):
        if platform.system() == "Linux":
            try:
                await message.channel.trigger_typing()
            except: pass
        else:
            return await message.add_reaction("❌")

        output = ""
        colorCode = False
        checkOutput = subprocess.check_output(["neofetch"]).decode("utf-8")
        for charIndex in range(len(checkOutput)):
            char = checkOutput[charIndex]
            if char.lower() in "abcdefghijklmnopqrstuvwxyz01234567890@_:/\\+-|.,]()\n " and not colorCode:
                output += char
            elif char == "`":
                output += "'"
            elif char == "[":
                if checkOutput[charIndex+1] in "0123456789?":
                    colorCode = True
                else:
                    output += "["
            if colorCode and char in "abcdefghijklmnopqrstuvwxyz":
                colorCode = False

        output = output.split("MiB \n")[0]+"MiB"
        output = output.replace("joe@", "\njoe@")
        embed = discord.Embed()
        embed.title = "NeoFetch"
        embed.description = "```"+output[:1990]+"```"
        await message.channel.send(embed=embed)

status.startTasks += [[status.presence]]

status.mentionedCommands["ping(?!\S)"] = [status.ping, ["message"], {}]
status.exclamationCommands["ping(?!\S)"] = [status.ping, ["message"], {}]
status.mentionedCommands["(stat(us|s)|about|info)(?!\S)"] = [status.status, ["message", "typing"], {"self":status}]
status.exclamationCommands["about(?!\S)"] = [status.status, ["message", "typing"], {"self":status}]
status.mentionedCommands["neofetch(?!\S)"] = [status.neofetch, ["message"], {"self":status}]
