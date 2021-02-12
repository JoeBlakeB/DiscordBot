import discord
import praw
import requests
import io

# embed = discord.Embed()
# embed.title = subreddit
# byt = io.BytesIO(requests.get(subreddit).content)
# file = discord.File(fp=byt, filename="nigga.png", spoiler=("spoiler" in command))
# embed.set_image(url="attachment://nigga.png")
# # embed.set_image(url="https://cdn.discordapp.com/attachments/643102110375870483/809892611442999317/HT1HhQW8.jpg")
#
# await message.channel.send("Subreddit: " + subreddit, embed=embed, file=file)

class reddit:
    help = {"list": True, "ListPriority": 5, "Title":"Reddit",
        "ShortHelp": "Get a post from a subreddit. **Currently work in progress.**",
        "LongHelp": "Get a post from a subreddit.\n"+
        "\n✔ make something to store the store the keys so I dont accidentally upload the api keys to github\n"+
        "❌ work out what the user wants the bot to do\n"+
        "❌ get random post from the front page\n"+
        "❌ get top post of all time\n"+
        "❌ get specific post from top\n"+
        "❌ get random post from top\n"+
        "❌ get most recent post from new\n"+
        "❌ embed the content\n"+
        "❌ embed reddit share link\n"+
        "❌ bugfixes\n"+
        "\nFuture commands:\n"+
        "**@{displayName} reddit** to get a post from the front page.\n"+
        "**@{displayName} reddit r/<subreddit>** or **@{displayName} r/<subreddit>** "+
        "to get a post from the front page of that subreddit.\n"+
        "**@{displayName} reddit r/<subreddit> [<hot/new>] [<number>]** to get a post from hot/new of a subreddit.\n"+
        "**@{displayName} reddit <share link>** to share a post from reddit and embed it."}

    async def __new__(self, message, command, parentClass):
        await dev(message, command, parentClass)
        for word in ["feet", "foot", "hentai", "rule34", "loli", "porn"]:
            if word in message.content:
                await message.channel.send("Fuck off degenerate.")
                return
        await message.channel.send("See **joebot help reddit** to see progress on the reddit command.")

class dev:
    try:
        prawReddit = praw.Reddit(user_agent="Joe#8648 - joeblakeb.github.io")
    except Exception as e:
        prawReddit = Exception
        prawException = e

    async def __new__(self, message, command, parentClass):
        if len(command) == 2:
            subreddit = "all"
        elif command[2][:2].lower() == "r/":
            subreddit = command[2][2:]
        else:
            subreddit = command[2]


        await message.channel.send("Subreddit: " + subreddit)
