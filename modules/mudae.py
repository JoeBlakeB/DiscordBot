import random

import baseClass

class mudae(baseClass.baseClass):
    messageList = ["https://tenor.com/view/dr-nefario-fart-gun-gif-20054143",
        "https://tenor.com/view/man-riding-pig-lets-ride-omw-gif-8516259",
        "https://tenor.com/view/punch-angry-mad-cat-tiger-gif-6222115",
        "https://media.discordapp.net/attachments/804466170694336572/804496644443471873/1354449706030657536-1.gif",
        "https://media.discordapp.net/attachments/818800470524690443/818903742807539712/image0.gif",
        "https://tenor.com/view/cats-falling-falling-cat-cattitude-chat-gif-17690548",
        "https://tenor.com/view/nickimperiod-gif-20207882",
        "https://tenor.com/view/fiddleafox-cat-gif-18590523",
        "https://tenor.com/view/cringe-floppa-sniff-gif-20819216",
        "https://tenor.com/view/pirates-davy-jones-dead-mans-chest-at-worlds-end-pirates-ofthe-caribbean-gif-14136409",
        "https://media.discordapp.net/attachments/441463102605754368/823638777159090196/image0-3.gif",
        "https://tenor.com/view/happy-birthday-ashleigh-smiling-dog-happy-gif-13607269",
        "https://media.discordapp.net/attachments/811720145478221883/814823184800284732/globe.gif",
        "https://tenor.com/view/sleep-hamster-good-morning-waking-up-gif-5187196",
        "https://tenor.com/view/smile-doggy-dog-smile-pet-happy-gif-17804041",
        "https://media.discordapp.net/attachments/787613837129285663/821836235278123017/a_247dab51ba9c1c6f904dd586ba8d5422.gif",
        "https://tenor.com/view/close-the-door-okay-im-out-bye-now-see-ya-neatdad-gif-16767040",
        "https://tenor.com/view/cat-standing-cat-scared-scared-cat-gif-12049194",
        "https://cdn.discordapp.com/emojis/809522514996625458.gif?v=1",
        "https://tenor.com/view/19dollar-fortnite-card-who-wants-it-and-yes-im-giving-it-away-remember-share-share-share-and-trolls-dont-get-blocked-gif-20067002",
        "https://cdn.discordapp.com/attachments/796434329831604288/836159855068446740/FloppaRoblox.gif",
        "https://i.redd.it/jfsl9u4i4fv61.gif",
        "https://tenor.com/view/supa-hot-fire-rekt-burn-popopo-im-not-a-rapper-gif-4910167",
        "https://cdn.discordapp.com/attachments/784512616461631498/835630485472149534/video0_-_2021-04-22T162803.577.mp4",
        "https://cdn.discordapp.com/attachments/784512616461631498/835626510244642836/you_are_really_pissing_me_off.mp4",
        "https://cdn.discordapp.com/attachments/643102110375870483/834799954269569095/video0-58.mp4",
        "https://cdn.discordapp.com/attachments/643102110375870483/834749363611238440/saul.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158873882722334/NigelFarageChungus.mov",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158874405830666/267c43d37780e2e229f081207b45ec36.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158876097052672/4910c6b964f40097b4dcb6a9bf85a264.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158878017781790/143506637_508974490065478_1575840665028811491_n.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158910728503296/video0_38.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158888826634250/BryanCat.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158896598417408/video_killed_the_radio_star.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158900305920010/video0_17.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836173788781346826/chrup.webm",
        "https://cdn.discordapp.com/attachments/796434329831604288/836741072733339690/WideJohn.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836741076714389565/WideKev.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836742675200868378/bububudadada.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836742127174156388/FloppaEars.gif",
        "https://cdn.discordapp.com/attachments/796434329831604288/836742129984208916/SCzingus.gif"]
    async def mudae(message):
        if ( "the roulette is limited to" in message.content and "uses per hour" in message.content and "Upvote Mudae to reset the timer: **$vote**. Twitter: **@​Mudaebot**" in message.content ) or message.content == "Command under maintenance!\n(For **5** minutes, weekly maintenance)":
            await message.channel.send(random.choice(mudae.messageList))

        try:
            embed = message.embeds[0]
            if "/" in str(embed.footer) and (("Claim Rank: #" in str(embed.description) and "Like Rank: #" in str(embed.description)) or "Page" in str(embed.footer)):
                await message.add_reaction("⬅️")
        except IndexError: pass

mudae.generalCommands += [["authorID", 432610292342587392, mudae.mudae, ["message"], {}]]
