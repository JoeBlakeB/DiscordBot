import discord
import sys
import subprocess

class stats:
    help = {"list": True, "ListPriority": 2, "Title":"Stats",
        "ShortHelp": "Get bot stats. *@{displayName} stats*",
        "LongHelp": "Gives stats for {displayName}.\n"+
        "Use **@{displayName} stats** to view bot stats."}

    def version():
        try:
            amountOfCommits = subprocess.check_output("git rev-list --count HEAD", shell=True, stderr=subprocess.STDOUT)
            return "\nJoeBot Version: " + str(amountOfCommits, "utf-8")
        except subprocess.CalledProcessError:
            return ""

    async def __new__(self, message, command, parentClass):
        embed = discord.Embed()
        embed.color = parentClass.__embedColor__()

        embed.title = "JoeBot Stats"
        embed.description = "Python Version: " + sys.version[:5] + "\nDiscord Version: " + discord.__version__
        embed.description += self.version()
        embed.description += "Server Count: " + str(len(parentClass.__bot__().guilds))

        await message.channel.send(embed=embed)
