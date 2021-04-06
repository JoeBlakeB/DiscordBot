import discord

import baseClass
import emojis

class test(baseClass.baseClass):
    pass

test.mentionedCommands["test"] = [test.__new__, ["message"], {"self":test, "text":"Hello World!"}]
test.mentionedCommands["hoodcate"] = [test.__new__, ["message"], {"self":test, "text":"<:hoodcate:802124875699191819>"}]
test.mentionedCommands["hood cate hd"] = [test.__new__, ["message"], {"self":test, "text":"<:hoodcateHD:822937932464914494>"}]
