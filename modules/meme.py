#!/usr/bin/env python3
# JoeBot Copyright (C) 2021 JoeBlakeB
__author__ = "JoeBlakeB"
__copyright__ = "Copyright 2021, JoeBlakeB (joeblakeb.github.io)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import asyncio
import discord
import io
import shlex
import sys
import traceback

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class meme:
    class discordBot:
        try:
            from baseClass import baseClass
        except: pass

        async def memepy(self, message, commandContent):
            #if message.author.id != 365154655313068032:
            #    return await message.channel.send("joebot meme maker is currently work in progress...")
            try:
                shlexOutput = shlex.split(message.content)
            except Exception:
                return await message.channel.send(traceback.format_exc().strip().split("\n")[-1])
            wordZero = message.content.split()[:(1+len(message.content.split())-len(commandContent.split()))]
            messageWords = [" ".join(wordZero)] + shlexOutput[len(wordZero):]
            output = await self.meme(self, messageWords)
            if isinstance(output, str):
                await message.channel.send("```\n"+output+"\n```")
            elif isinstance(output, io.BytesIO):
                image = discord.File(fp=output, filename="i_want_to_die.png")
                await message.channel.send(file=image)

        async def meme(self, message):
            if message.author.id != 365154655313068032:
                return await message.channel.send("joebot meme maker is currently work in progress, use meme.py instead")
            # await message.channel.send("The easy to use interface is work in progress, use meme.py instead for CLI usage.")

    def __new__(*args, **kwargs):
        return asyncio.run(meme.meme(*args, **kwargs))

    async def meme(self, argv):
        if len(argv) <= 1 or "help" in argv:
            return meme.help.format(argv)
        # return "NOT IMPLEMENTED " + str(argv)
        try:
            fontname = argv[2]
        except:
            fontname = "impact.ttf"
        fontsize = 100
        text = argv[1]

        colorShaddow = (0, 0, 0, 255)
        colorText = (255, 255, 255, 255)
        colorBackground = (255, 255, 255, 0)


        font = ImageFont.truetype(fontname, fontsize)
        testImg = Image.new('RGBA', (1, 1))
        testDraw = ImageDraw.Draw(testImg)
        width, height = testDraw.textsize(text, font)
        print(width, height, flush=True)
        img = Image.new('RGBA', (width+4, height+4), colorBackground)
        d = ImageDraw.Draw(img)
        d.text((-4, -4), text, fill=colorShaddow, font=font)
        d.text((-4, 4), text, fill=colorShaddow, font=font)
        d.text((4, -4), text, fill=colorShaddow, font=font)
        d.text((4, 4), text, fill=colorShaddow, font=font)

        d.text((0, 0), text, fill=colorText, font=font)

        byteIO = io.BytesIO()
        img.save(byteIO, format='PNG')
        return io.BytesIO(byteIO.getvalue())

    help = """JoeBot Meme Maker
Usage: {0[0]} [OPTIONS]

- Options are case sensitive

Options:
- help             - Gives this help message then exits
""".strip()

if __name__ == '__main__': # so this can be used as a standalone script
    output = meme(sys.argv)
    if isinstance(output, str):
        print(output, flush=True)
    else: #elif isinstance(output, bytesio or something idk i cant remember):
        print("OUTPUTTING TO FILE NOT IMPLEMENTED YET", flush=True)
else:
    try: # for joebot
        meme.discordBot.baseClass.mentionedCommands["(|./)meme.py(?!\S)"] = [meme.discordBot.memepy, ["message", "commandContent"], {"self":meme}]
        meme.discordBot.baseClass.exclamationCommands["meme.py(?!\S)"] = [meme.discordBot.memepy, ["message", "commandContent"], {"self":meme}]
        meme.discordBot.baseClass.mentionedCommands["meme(?!\S)"] = [meme.discordBot.meme, ["message"], {"self":meme}]
        meme.discordBot.baseClass.exclamationCommands["meme(?!\S)"] = [meme.discordBot.meme, ["message"], {"self":meme}]
    except: pass
