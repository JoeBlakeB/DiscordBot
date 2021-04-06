import discord
import random

class userJoinLeave:
    joinMessages = ["I should probably warn you that {name} is a registered sex offender.", "Hello {name}"]
    leaveMessages = ["{name} leaving is kinda poggers.", "Yay, {name} left", "Bye {name}"]

    async def __new__(self, member, joined):
        if joined: messageList = self.joinMessages
        else: messageList = self.leaveMessages

        for channelName in ["welcome", "general"]:
            channel = discord.utils.get(member.guild.text_channels, name=channelName)
            if channel != None:
                try:
                    await channel.send(random.choice(messageList).format(name=member.display_name))
                    return
                except: pass
