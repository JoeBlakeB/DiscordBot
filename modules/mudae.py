import random

import baseClass

class mudae(baseClass.baseClass):
    gifList = ["https://tenor.com/view/dr-nefario-fart-gun-gif-20054143",
        "https://tenor.com/view/man-riding-pig-lets-ride-omw-gif-8516259",
        "https://tenor.com/view/punch-angry-mad-cat-tiger-gif-6222115",
        "https://media.discordapp.net/attachments/804466170694336572/804496644443471873/1354449706030657536-1.gif",
        "https://media.discordapp.net/attachments/818800470524690443/818903742807539712/image0.gif",
        "https://tenor.com/view/cats-falling-falling-cat-cattitude-chat-gif-17690548",
        "https://tenor.com/view/nickimperiod-gif-20207882",
        "https://tenor.com/view/fiddleafox-cat-gif-18590523"]
    async def limit(message):
        if "the roulette is limited to" in message.content and "uses per hour" in message.content and "Upvote Mudae to reset the timer: **$vote**. Twitter: **@​Mudaebot**" in message.content:
            await message.channel.send(random.choice(mudae.gifList))

mudae.generalCommands += [["authorID", 432610292342587392, mudae.limit, ["message"], {}]]
