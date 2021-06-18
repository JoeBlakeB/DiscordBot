import asyncio
import baseClass
import discord
import emojis
import traceback

class admin(baseClass.baseClass, baseClass.baseUtils):
    async def common(message):
         await message.add_reaction("❌")
         await message.channel.send(message.author.display_name + " is not in the sudoers file.  This incident will be reported.")

    async def react(message):
        if message.author.id != 365154655313068032:
            return await admin.common(message)
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            if message.content[15:] in list(emojis.emojis):
                await referenceMessage.add_reaction(emojis.emojis[message.content[15:]])
            else:
                await referenceMessage.add_reaction(message.content[15:].replace(";", ":"))
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

    async def say(message):
        if message.author.id != 365154655313068032:
            return await admin.common(message)
        try:
            await message.channel.send(message.content[15:].replace(";", ":"))
            await admin.deleteMessage(message, time=10)
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

    async def servers(message, bot):
        if message.author.id != 365154655313068032:
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
        if message.author.id != 365154655313068032:
            return await admin.common(message)
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            await referenceMessage.edit(content=message.content[17:].replace(";", ":"))
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

admin.mentionedCommands["sudo react(?!\S)"] = [admin.react, ["message"], {}]
admin.mentionedCommands["sudo say(?!\S)"] = [admin.say, ["message"], {}]
admin.mentionedCommands["sudo server list(| verbose)"] = [admin.servers, ["message", "bot"], {}]
admin.mentionedCommands["sudo edit(?!\S)"] = [admin.edit, ["message"], {}]
