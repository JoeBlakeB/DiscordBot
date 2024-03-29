import aiohttp
import asyncio

class baseClass:
    mentionedCommands = {}
    exclamationCommands = {}
    generalCommands = []
    startTasks = []
    closeTasks = []
    help = {}

class baseUtils:
    async def deleteMessage(message, time=3, reaction="✅"):
        try:
            await message.add_reaction(reaction)
            await asyncio.sleep(time)
            await message.delete()
        except Exception:
            pass

    async def aiohttpGet(url, headers={"User-Agent": "JoeBlakeB-Discord-Bot/1.0 (https://github.com/JoeBlakeB/DiscordBot)"}, json=False, bytes=False):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if json:
                    try:
                        return await resp.json(), resp.status
                    except aiohttp.client_exceptions.ContentTypeError:
                        raise ValueError
                elif bytes:
                    return await resp.read(), resp.status
                else:
                    return await resp.text(), resp.status

# mentionedCommands & exclamationCommands
# exampleClass.mentionedCommands[regex] = [asyncFunctionToRun, argList, staticArgsDict]
# example:                       args in joebot.py>bot.runCommand ^            ^ for things like passing self to functions
# exampleClass.mentionedCommands[regex, example: "test(?!\S)"] = [exampleClass.function, [args, example: "message"], {kwargs, examples: "self":exampleClass, "text":"<:hoodcateHD:822937932464914494>"}]

# generalCommands example:         (will run for every message so is innefficient, use mentionedCommands or exclamationCommands instead where possible)
# exampleClass.generalCommands += [[checkType, checkData, asyncFunctionToRun, argList, staticArgsDict]]
# example:
# exampleClass.generalCommands += [["authorID", 365154655313068032, exampleClass.function, ["message"], {}]]

# startTasks & closeTasks
# (runs when the bot starts/is stopped with a keyboard interrupt)
# (must be a coroutine, example: async def startup())
# example:
# exampleClass.startTasks += [exampleClass.startup(args)]
## note: exampleClass.startTasks += [[exampleClass.startup()]] can be used if the only required arg is the bot object

# list of args for mentionedCommands, exclamationCommands & generalCommands
#  message              - discord message object
#  messageContentLower  - messageContentLower from the on_message, with any @JoeBots replaced with just joebot
#  commandContent       - messageContentLower but without any of the joebot or !, example: "joebot hello" > "hello". not intended for generalCommands
#  bot                  - bot object
#  typing               - triggers typing, doesnt actually pass any extra data

# list of checkTypes for generalCommands
#  authorID             - runs only for certain user
#  authorDisplayNameRegex          - regex of the authors display_name

# example module for a module that will say "Hello world!" when someone says "joebot hello"
#./modules/example.py
#
# import baseClass
#
# class example(baseClass.baseClass):
#     async def hello(message):
#         await message.channel.send("Hello world!")
#
# example.mentionedCommands["hello"] = [example.hello, ["message"], {}]

# help
# for an embedded help
# example.help = ["embed", {"title":"example title", "description":"example desciption", "thumbnail":"https://cdn.discordapp.com/emojis/690344425356001320.png"}]
# for an embedded help that is shown in base help
# example.help = ["embed,include", {"title":"example title", "description":"example desciption", "thumbnail":"https://cdn.discordapp.com/emojis/690344425356001320.png"}]
# for a plaintext help
# example.help = ["plaintext", "example plaintext help"]
# for include only
# example.help = ["include", "example plaintext help"]
