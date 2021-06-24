#!/usr/bin/env python3

import base64
import discord
import io
try:
    import mcstatus
except:
    mcstatus = False
from PIL import Image

import baseClass

class minecraftPing(baseClass.baseClass):
    async def ping(message, messageContentLower):

        messageContentLower = messageContentLower[14-(bool(messageContentLower[0] == "!")*6):]
        if messageContentLower.startswith("ftping "):
            messageContentLower = messageContentLower[7:]
        messageContentLower = messageContentLower.strip().replace(":", " ").split(" ")
        ip = "localhost"
        port = 25565
        if messageContentLower[0] != "": ip = messageContentLower[0]
        if len(messageContentLower) >= 2:
            try:
                port = int(messageContentLower[1])
            except: pass

        server = mcstatus.MinecraftServer(ip, port)
        try:
            status = await server.async_status()
            raw = status.raw
        except Exception:
            raw = {"description":"Can't connect to server"}
        embed = discord.Embed()
        if isinstance(raw["description"], dict):
            if raw["description"]["text"] == "":
                motd = ""
                for extra in raw["description"]["extra"]:
                    motd += extra["text"].strip(" ")
            else:
                motd = raw["description"]["text"]
        else:
            motd = raw["description"]

        embed.title = ""
        ignoreNext = False
        for char in motd:
            if ignoreNext:
                ignoreNext = False
            elif char == "§":
                ignoreNext = True
            else:
                embed.title += char

        embed.description = "Server Address: " + ip
        if port != 25565:
            embed.description += str(port)
        if "players" in raw:
            if "online" in raw["players"]:
                embed.description += "\nPlayers: " + str(raw["players"]["online"])
                if "max" in raw["players"]:
                    embed.description += "/" + str(raw["players"]["max"])
        if "version" in raw:
            if "name" in raw["version"]:
                embed.description += "\nVersion: " + str(raw["version"]["name"])
                # if "protocol" in raw["version"]:
                #     embed.description += "\nServer Protocol: " + str(raw["version"]["protocol"])

        if "favicon" in raw: # This seems like some of it is pointless but I cant get it to work any other way
            image = base64.b64decode(raw["favicon"].split("data:image/png;base64,")[1])
            resize = Image.open(io.BytesIO(image)).resize((128,128))
            byteIO = io.BytesIO()
            resize.save(byteIO, format='PNG')
            bytesio = io.BytesIO(byteIO.getvalue())
            image = discord.File(fp=bytesio, filename="server_icon.png")
            embed.set_thumbnail(url="attachment://server_icon.png")
            await message.channel.send(embed=embed, file=image)
        else: # greyed out pack.png image
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/797142065851007016/857224357918670868/unknown_server.png")
            await message.channel.send(embed=embed)


if mcstatus:
    minecraftPing.mentionedCommands["(minecraft|mc)ping(?!\S)"] = [minecraftPing.ping, ["message", "messageContentLower"], {}]
    minecraftPing.exclamationCommands["(minecraft|mc)ping(?!\S)"] = [minecraftPing.ping, ["message", "messageContentLower"], {}]
    minecraftPing.help["MinecraftPing"] = ["include", None]
    minecraftPing.help["(mc|minecraft)ping"] = ["embed", {"title":"Minecraft Server Ping", "description":"Ping a Minecraft server\n\nUse **minecraftping** or **mcping** and say the servers IP or domain after.\n\nSyntax:\n<@796433833296658442> minecraftping <IP>:<PORT>\n!mcping <IP>", "thumbnail":"https://cdn.discordapp.com/emojis/613523198377590935.gif"}]
