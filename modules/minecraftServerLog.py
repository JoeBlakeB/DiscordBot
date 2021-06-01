import asyncio
import discord
import random
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

class minecraftServerLog(baseClass.baseClass):
    startTime = datetime.datetime.fromtimestamp(time.time()).strftime("[%H:%M:%S]")
    async def monitor(bot):
        sayLogQueue = []
        logFile = "/home/joe/Games/MinecraftServer/logs/latest.log"
        newFile = False
        await asyncio.sleep(4)
        while True:
            channel = bot.client.get_channel(847903522741813299)
            try:
                with open(logFile, "r") as file:
                    firstLine = file.readline()
                    file.seek(1)
                    while True:
                        if newFile:
                            break
                        if not file.readline():
                            break
                    while True:
                        where = file.tell()
                        line = file.readline()
                        if not line:
                            if sayLogQueue != []:
                                await minecraftServerLog.sayLog(channel, sayLogQueue)
                                sayLogQueue = []
                            await asyncio.sleep(12)
                            file2 = open(logFile, "r")
                            file2Firstine = file2.readline()
                            file2.close()
                            if file2Firstine != firstLine:
                                print("NEW FILE", flush=True)
                                newFile = True
                                raise Exception("NewFile")
                            file.seek(where)
                        else:
                            sayLogQueue.append(line)
            except Exception as e:
                if str(e) != "NewFile":
                    print(traceback.format_exc(), flush=True)
                await asyncio.sleep(20)

    async def sayLog(channel, sayLogQueue):
        say = sayLogQueue[0]
        for line in sayLogQueue[1:]:
            if len(say+line) <= 2000:
                say += line
            else:
                await channel.send(say.strip())
                say = ""
                await asyncio.sleep(1)
        if say != "":
            await channel.send(say.strip())

# minecraftServerLog.startTasks += [[minecraftServerLog.monitor]]
