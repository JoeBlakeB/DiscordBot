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
        "https://tenor.com/view/duck-happy-dance-dansando-feliz-gif-21214947",
        "https://tenor.com/view/supa-hot-fire-rekt-burn-popopo-im-not-a-rapper-gif-4910167",
        "https://cdn.discordapp.com/attachments/784512616461631498/835630485472149534/video0_-_2021-04-22T162803.577.mp4",
        "https://cdn.discordapp.com/attachments/784512616461631498/835626510244642836/you_are_really_pissing_me_off.mp4",
        "https://cdn.discordapp.com/attachments/643102110375870483/834799954269569095/video0-58.mp4",
        "https://cdn.discordapp.com/attachments/643102110375870483/834749363611238440/saul.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158873882722334/NigelFarageChungus.mov",
        "https://cdn.discordapp.com/attachments/796434329831604288/836158874405830666/267c43d37780e2e229f081207b45ec36.mp4",
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
        "https://cdn.discordapp.com/attachments/796434329831604288/836742129984208916/SCzingus.gif",
        "https://v.redd.it/eplua59kpvx61/DASH_480.mp4",
        "https://cdn.discordapp.com/attachments/671678084717740043/840587502162935808/hoodcate_gone_wild.mp4",
        "https://cdn.discordapp.com/attachments/780911133388177428/822022618378534912/Mister_Mellow_-_DadWorksForSega-1338990937192755200.mp4",
        "https://cdn.discordapp.com/attachments/671678084717740043/826222413339426876/hoodcate_interrogate.mp4",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643770499727360/HoodCateSleep3.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643764204732436/HoodCateSleep2.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643757447446528/HoodCateSleep.png",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643748618960896/HoodCateHD.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643742398414888/HoodCateChill.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643740137160725/HoodCateAd.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643738568753182/HoodCate2.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643736097783838/HoodCate.png",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643733934702632/DontMessWithHoodCate.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643786907451422/YoungHoodCate2.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643783985332254/YoungHoodCate.jpg",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643788036243466/image0.png",
        "https://cdn.discordapp.com/attachments/796434329831604288/840643775294734366/HoodCateSmug.png",
        "https://cdn.discordapp.com/attachments/808556111321628672/840666046037360660/video0-12.mp4",
        "https://www.youtube.com/watch?v=OwOnt8pohNw",
        "https://www.youtube.com/watch?v=UHPwxIC27uU",
        "https://www.youtube.com/watch?v=AyOqGRjVtls",
        "https://www.youtube.com/watch?v=cvh0nX08nRw",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=rGCxtPLzwO8",
        "https://www.youtube.com/watch?v=doEqUhFiQS4",
        "https://www.youtube.com/watch?v=C29IvglSGX0",
        "https://i.redd.it/lz8vahs07py61.gif\nhttps://i.redd.it/v503ed557py61.gif",
        "https://cdn.discordapp.com/attachments/643102110375870483/843112139383635989/6f72abee298454172ffba931982e8ad3.mp4",
        "https://cdn.discordapp.com/attachments/735496384974946425/846795614473683054/hoodvibe.mp4",
        "https://cdn.discordapp.com/attachments/643102110375870483/861188652528828436/BryanHussein.jpeg",
        "https://cdn.discordapp.com/attachments/643102110375870483/851155937049444402/HoodCateGif.gif",
        "https://cdn.discordapp.com/attachments/873982079677894657/874022282765426688/Gaming.webm",
        "https://media.discordapp.net/attachments/869988741572350003/873869997250850826/image0-18.gif",
        "https://media.discordapp.net/attachments/869988741572350003/873869997250850826/image0-18.gif\nhttps://tenor.com/view/cat-stealer-gif-21321506",
        "https://cdn.discordapp.com/attachments/873982079677894657/874023375637450832/cat-bot-very-cool_20210529_3-1.mp4",
        "https://cdn.discordapp.com/attachments/873982079677894657/874023335539900466/redditsave.com_breaking_bad-b2oom28al3b71-360.mp4",
        "https://tenor.com/view/loading-discord-loading-discord-boxes-squares-gif-16187521",
        "https://tenor.com/view/tom-scott-vaping-smoking-coughing-nazarino-gif-20386028",
        "https://cdn.discordapp.com/attachments/842076301350273069/873203577621975080/dumpy873203450115158046.gif",
        "https://i.redd.it/2cty5caff3e71.gif",
        "https://cdn.discordapp.com/attachments/784512616461631498/874755352753733662/trolling.gif",
        "https://tenor.com/view/nig-nibba-nigmode-dzsordzs-szia-gif-21468466\nhttps://tenor.com/view/ger-nibba-nigmode-dzsordzs-sz%C3%ADvd-ki-af-gif-21468467"]
    async def mudae(message):
        if ( "the roulette is limited to" in message.content and "uses per hour" in message.content and "Upvote Mudae to reset the timer: **$vote**. Twitter" in message.content ) or message.content == "Command under maintenance!\n(For **5** minutes, weekly maintenance)" or "For this server, you can claim once per interval of 3h. The next interval begins in" in message.content or "One rolls reset per interval.\nTime left:" in message.content or ", You can't react to kakera for" in message.content or (", you can't claim for another " in message.content and len(message.content) < 80):
            await message.channel.send(random.choice(mudae.messageList))

mudae.generalCommands += [["authorID", 432610292342587392, mudae.mudae, ["message"], {}]]
