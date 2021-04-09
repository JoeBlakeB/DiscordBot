import asyncio

class baseClass:
    mentionedCommands = {}
    exclamationCommands = {}
    startTasks = []
    closeTasks = []

class baseUtils:
    async def deleteMessage(message, time=3):
        try:
            await message.add_reaction("✅")
            await asyncio.sleep(time)
            await message.delete()
        except Exception:
            pass

# example.mentionedCommands[regex, example: "test(?!\S)"] = [example.function, [args, example: "message"], {kwargs, examples: "self":test, "text":"<:hoodcateHD:822937932464914494>"}]
