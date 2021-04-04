#!/usr/bin/env python3

import random
import discord
import asyncio

class good:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() in ["bot", "boy"]:
            await message.channel.send(random.choice([":3", "uwu", "UωU"]))
        else:
            raise Exception
class bad:
    async def __new__(self, message, command, parentClass):
        if command[2].lower() in ["bot", "boy"]:
            await message.channel.send(random.choice(["ÓnÒ why am I a bad bot?", "ÒwÓ no you", "thats mean"]))
        else:
            raise Exception

class hi:
    async def __new__(self, message, command, parentClass):
        await message.channel.send(random.choice(["Hello", "Hi", "Hey", "uwu hi", ":3 hey", "Hello there", "Hewwo"]))

hey = hi
hello = hi

class say:
    async def __new__(self, message, command, parentClass):
        if len(command) <= 2:
            raise IndexError
            return
        await message.channel.send(" ".join(command[2:]))
        try:
            await message.add_reaction("✅")
            await asyncio.sleep(3)
            await message.delete()
        except: pass

class gun:
    async def __new__(self, message, command, parentClass):
        await message.channel.send(self.gun(parentClass))
    def gun(parentClass):
        bot = parentClass.__bot__()
        gun = ""
        for i in range(1,5):
            gun += str(discord.utils.get(bot.emojis, name="shotgun"+str(i)))
        return gun

class kill:
    help = {"list": True, "ListPriority": 10, "Title":"Kill",
        "ShortHelp": "Kill someone *@{displayName} kill <name>*",
        "LongHelp": "Kill someone.\n"+
        "Use **@{displayName} kill <name>**"}
    async def __new__(self, message, command, parentClass):
        if len(command) <= 2:
            await message.channel.send("You need to say who you want to kill.")
            return
        await message.channel.send(message.author.display_name + " " + gun.gun(parentClass) + " " + " ".join(command[2:]))

class pogchamp:
    async def __new__(self, message, command, parentClass):
        for i in range(random.randint(4,16)):
            await message.channel.send("PogChamp")
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
        await message.channel.send("PogChamp")

class porn:
    help = {"list": False, "Title":"Porn",
        "LongHelp": "Porn.\n"+
        "Use **@{displayName} porn**"}
    urls = ["3chJDM7", "3t3GQvM", "36gTVIs", "36kYhyj", "2KWKKWh", "2MeJUVt", "3iVIj2F", "2YpG522",
        "2NIS6Oa", "2Yl6zBI", "3qVKCFR", "3iVUpJc", "3j6gXap", "3ae9aD1", "2YkFTRB", "3cic5xi",
        "3pvyOtI", "39nIz7x", "3r3UOfB", "36C2Nsz", "39mMKjT", "36nD07g", "3t7GSmG", "3oxL5MY",
        "3oqE8gC", "3ahTgrE", "3iTpTQ0", "2YtoPZH", "3t5V3sk"]
    async def __new__(self, message, command, parentClass):
        embed = discord.Embed()
        embed.title = random.choice(["Here you go.", "Keep the change you filthy animal", "Here, now fuck off.", "Fine"])
        embed.color = parentClass.__embedColor__()
        embed.url = "https://bit.ly/" + random.choice(self.urls)
        await message.channel.send(embed=embed)

class __admin__:
    owner = 365154655313068032
    async def __new__(self, message, command, parentClass):
        try:
            if "__" in command[2]:
                raise Exception
            commandattr = getattr(self, command[2].lower())
        except:
            # Command Not Found
            return await message.add_reaction("❓")

        adminRole = False
        for role in message.author.roles:
            if str(role).lower() in ["admin"]: adminRole = True
        if (not adminRole) and (message.author.id != self.owner):
            # Access Denied
            return await message.add_reaction("⛔")

        try:
            if not await commandattr(self, message, command, parentClass):
                return await message.add_reaction("✅")
        except Exception as e: # Error
            await message.add_reaction("⚠️")
            if command[1] == "#":
                await message.channel.send(e)

    async def __delete(message, react, time):
        try:
            await message.add_reaction(react)
            await asyncio.sleep(time)
            await message.delete()
        except: pass
        return True

    async def nick(self, message, command, parentClass):
        await message.guild.me.edit(nick=" ".join(command[3:]))

    async def nick2(self, message, command, parentClass):
        if len(command) == 3:
            await message.add_reaction("❓")
            return True, await message.channel.send("joebot ! nick2 <userID> <nick>")
        await message.guild.get_member(int(command[3])).edit(nick=" ".join(command[4:]))

    async def perms(self, message, command, parentClass):
        await message.channel.trigger_typing()
        await message.channel.send([perm[0] for perm in message.guild.me.guild_permissions if perm[1]])

    async def delete(self, message, command, parentClass):
        referenceMessage = await message.channel.fetch_message(message.reference.message_id)
        await referenceMessage.delete()
        return await self.__delete(message, "✅", 3)

    async def __role(self, message, command, parentClass, roleFunc):
        if message.author.id != self.owner:
            return True, await message.add_reaction("⛔")
        if len(command) == 3:
            await message.add_reaction("❓")
            return True, await message.channel.send("joebot ! "+roleFunc+" <userID> <roleName>")
        userID = ""
        for character in command[3]:
            if character in "0123456789":
                userID += character
        member = message.guild.get_member(int(userID))
        if roleFunc == "addRole": roleFunction = member.add_roles
        else: roleFunction = member.remove_roles
        await roleFunction(discord.utils.get(message.guild.roles, name=" ".join(command[4:])))

    async def addrole(self, message, command, parentClass):
        return await self.__role(self, message, command, parentClass, "addRole")

    async def removerole(self, message, command, parentClass):
        return await self.__role(self, message, command, parentClass, "removeRole")

    async def edit(self, message, command, parentClass):
        referenceMessage = await message.channel.fetch_message(message.reference.message_id)
        await referenceMessage.edit(content=message.content[len(" ".join(command[:3])):])
        return await self.__delete(message, "✅", 3)
