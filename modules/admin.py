import asyncio
import baseClass
import emojis
import traceback

class admin(baseClass.baseClass, baseClass.baseUtils):
    async def react(message):
        if message.author.id != 365154655313068032:
            return await message.add_reaction("❌")
        try:
            referenceMessage = await message.channel.fetch_message(message.reference.message_id)
            if message.content[8:] in list(emojis.emojis):
                await referenceMessage.add_reaction(emojis.emojis[message.content[8:]])
            else:
                await referenceMessage.add_reaction(message.content[8:].replace(";", ":"))
            await admin.deleteMessage(message)
        except:
            await message.add_reaction("⚠️")

    async def say(message):
        if message.author.id != 365154655313068032:
            return await message.add_reaction("❌")
        try:
            await message.channel.send(message.content[6:].replace(";", ":"))
            await admin.deleteMessage(message, time=10)
        except:
            await message.add_reaction("⚠️")
            print(traceback.format_exc(), flush=True)

admin.exclamationCommands["!react(?!\S)"] = [admin.react, ["message"], {}]
admin.exclamationCommands["!say(?!\S)"] = [admin.say, ["message"], {}]
