import asyncio
import baseClass
import discord
import re
import traceback

class admin(baseClass.baseClass, baseClass.baseUtils):
    adminID = 365154655313068032

    async def common(message):
         await message.add_reaction("❌")
         await message.channel.send(message.author.display_name + " is not in the sudoers file.  This incident will be reported.")
         print(message.author.display_name, "tried to run admin command", message.content, flush=True)

    async def react(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            await referenceMessage.add_reaction(message.content[15:].replace(";", ":"))
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

    async def say(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            await message.channel.send(message.content[15:].replace(";", ":"))
            await admin.deleteMessage(message, time=10)
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def servers(message, bot):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            if "verbose" in message.content:
                for guild in bot.client.guilds:
                    embed = discord.Embed()
                    embed.title = guild.name
                    embed.description = "Members:\n"
                    embed.set_image(url=guild.icon_url)
                    for member in guild.members:
                        embed.description += "- " + member.name + "#" + member.discriminator + " (" + member.display_name + ")\n"
                    if len(embed.description) >= 2048:
                        embed.description = "\n".join(embed.description[:2048].split("\n"))
                    await message.channel.send(embed=embed)
            else:
                serverList = []
                for guild in bot.client.guilds:
                    serverList.append(guild.name)
                await message.channel.send(str(serverList))
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def edit(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            await referenceMessage.edit(content=message.content[17:].replace(";", ":"))
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

    async def dmSend(message, bot):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            reciever = message.content[20:].split(" ")[0]
            content = message.content[21+len(reciever):].replace(";", ":")
            reciever = re.findall(r"\d+", reciever)[0]
            user = bot.client.get_user(int(reciever))
            await user.send(content)
            await message.add_reaction("✅")
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def dmHistory(message, bot):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            reciever = message.content[23:].split(" ")[0]
            reciever = re.findall(r"\d+", reciever)[0]
            user = bot.client.get_user(int(reciever))

            send = ""
            for userMessage in await user.history().flatten():
                sendAdd = userMessage.author.display_name + " - " + userMessage.content + "\n"
                if len(send) + len(sendAdd) > 2000:
                    await message.channel.send(send)
                    send = sendAdd
                else:
                    send += sendAdd
            await message.channel.send(send)
            await message.add_reaction("✅")
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def supress(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            await referenceMessage.edit(suppress=True)
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

    async def nick(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            await message.guild.me.edit(nick=message.content[17:])
        except:
            await message.add_reaction("⚠️")

    async def emoji(message):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            with open(message.content[18:], "rb") as img:
                img_byte = img.read()
                await message.guild.create_custom_emoji(name = (message.content.split("/")[-1].split(".")[0]), image = img_byte)
            await message.add_reaction("✅")
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def addRoleToEveryone(message, bot):
        if message.author.id != admin.adminID:
            return await admin.common(message)
        try:
            reacted = 1
            emoji1 = "<a:CatGif:797138290528354336>"
            emoji2 = "<a:clubAmogus:921166149754949672>"
            roleID = message.content.split(" ")[-1]
            try:
                roleID = int(roleID)
            except:
                roleID = int(roleID[3:-1])
            role = message.guild.get_role(roleID)
            for member in message.guild.members:
                await member.add_roles(role)
                if reacted == 1:
                    await message.add_reaction(emoji1)
                    await message.remove_reaction(emoji2, bot.client.user)
                    reacted = 2
                else:
                    await message.add_reaction(emoji2)
                    await message.remove_reaction(emoji1, bot.client.user)
                    reacted = 1
                await asyncio.sleep(4)
            await message.add_reaction("✅")
            await message.remove_reaction(emoji1, bot.client.user)
            await message.remove_reaction(emoji2, bot.client.user)
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

admin.mentionedCommands["sudo react(?!\S)"] = [admin.react, ["message"], {}]
admin.mentionedCommands["sudo say(?!\S)"] = [admin.say, ["message"], {}]
admin.mentionedCommands["sudo server list(| verbose)"] = [admin.servers, ["message", "bot"], {}]
admin.mentionedCommands["sudo edit(?!\S)"] = [admin.edit, ["message"], {}]
admin.mentionedCommands["sudo dm send(?!\S)"] = [admin.dmSend, ["message", "bot"], {}]
admin.mentionedCommands["sudo dm history(?!\S)"] = [admin.dmHistory, ["message", "bot"], {}]
admin.mentionedCommands["sudo sup(|p)res(|s)(?!\S)"] = [admin.supress, ["message"], {}]
admin.mentionedCommands["sudo nick(?!\S)"] = [admin.nick, ["message"], {}]
admin.mentionedCommands["sudo emoji(?!\S)"] = [admin.emoji, ["message"], {}]
admin.mentionedCommands["sudo addroletoeveryone(?!\S)"] = [admin.addRoleToEveryone, ["message", "bot"], {}]
