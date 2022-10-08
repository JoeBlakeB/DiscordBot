import datetime
import discord
import io
from PIL import Image
import re

import baseClass

class minecraftUser(baseClass.baseClass, baseClass.baseUtils):
    usernameRegex = re.compile("^\w+$")
    uuidRegex = re.compile("[0-9a-f]{8}(-|)[0-9a-f]{4}(-|)[0-9a-f]{4}(-|)[0-9a-f]{4}(-|)[0-9a-f]{12}")

    async def getUsername(self, message):
        try:
            await message.channel.trigger_typing()
        except: pass

        username = message.content.split(" ")[-1]
        if len(username) == 0:
            return await message.channel.send("You need to tell me a username to get.")
        elif (len(username) > 16 or not self.usernameRegex.match(username)) and not self.uuidRegex.match(username):
            return await message.channel.send("That is not a valid username.")

        try:
            await message.channel.send(embed=(await self.embedPlayerInfo(self, username)))
        except ValueError:
            await message.channel.send("Could not find that user.")
        except:
            await message.channel.send("Error: Could not get that users profile.")

    async def embedPlayerInfo(self, username):
        if len(username) > 16:
            profile = await self.getProfileFromUUID(self, username)
        else:
            profile = await self.getProfileFromUUID(self, username, url="https://api.mojang.com/users/profiles/minecraft/")
        embed = discord.Embed()

        if profile["name"][-1] == "s":
            titleAdd = "' Profile"
        else:
            titleAdd = "'s Profile"
        if profile["name"].lower() == profile["name"]:
            titleAdd = titleAdd.lower()
        embed.title = profile["name"] + titleAdd
        
        embed.description = f"**UUID**\n`{profile['id']}`\n`{profile['id'].replace('-', '')}`\n\n**Skin:**\n[Skin File](https://crafatar.com/skins/{profile['id']}?overlay)\n[Head Render](https://crafatar.com/renders/head/{profile['id']}?overlay) - [(no layers)](https://crafatar.com/renders/head/{profile['id']})\n[Body Render](https://crafatar.com/renders/body/{profile['id']}?overlay) - [(no layers)](https://crafatar.com/renders/body/{profile['id']})"

        embed.set_image(url="https://crafatar.com/renders/body/"+profile["id"]+"?overlay")
        embed.set_thumbnail(url="https://crafatar.com/avatars/"+profile["id"]+"?overlay")

        embed.color = await self.getColor(self, "https://crafatar.com/skins/"+profile["id"])

        return embed

    async def getProfileFromUUID(self, uuid, url="https://api.mojang.com/user/profile/"):
        mojangProfile = await self.aiohttpGet(url + uuid, json=True)
        profile = mojangProfile[0]
        id = profile["id"]
        profile["id"] = f"{id[:8]}-{id[8:12]}-{id[12:16]}-{id[16:20]}-{id[20:]}"
        return profile

    async def getColor(self, url):
        response = await self.aiohttpGet(url, bytes=True)
        img = Image.open(io.BytesIO(response[0]))
        colors = list(img.getdata())
        r, g, b = 0, 0, 0
        count = 0
        for pixel in colors:
            if pixel[3] == 255:
                count += 1
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
        return discord.Color.from_rgb(int(r/count), int(g/count), int(b/count))

minecraftUser.mentionedCommands["(minecraft|mc)(user|profile|skin)(?!\S)"] = [minecraftUser.getUsername, ["message"], {"self":minecraftUser}]
minecraftUser.exclamationCommands["(minecraft|mc)(user|profile|skin)(?!\S)"] = [minecraftUser.getUsername, ["message"], {"self":minecraftUser}]
minecraftUser.help["MinecraftProfile"] = ["include", None]
minecraftUser.help["minecraft(user|profile|skin)"] = ["embed", {"title":"Minecraft User Profile", "description":"Get a Minecraft (java) players profile\n\nUse **MinecraftProfile** and say the username or UUID after.\n\nSyntax:\n<@796433833296658442> minecraftprofile <username/UUID>", "thumbnail":"https://cdn.discordapp.com/emojis/613523198377590935.gif"}]
