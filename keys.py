#!/usr/bin/env python3
## Tokens, api keys, and secrets should be kept in keys.txt and read by keys.read
## keys.txt
##  | Discord: <Discord token>

# with open("token.txt") as tokenFile:
#    token = tokenFile.read().strip()

def read(*IDs):
    with open("keys.txt") as keysFile:
        keysRead = keysFile.read().strip()
    keys = {}
    for key in keysRead.split("\n"):
        keys[key.split(": ")[0]] = key.split(": ")[1]
    if len(IDs) == 1:
        return keys[IDs[0]]
    returnKeys = ()
    for ID in IDs:
        returnKeys += (keys[ID],)
    return returnKeys
