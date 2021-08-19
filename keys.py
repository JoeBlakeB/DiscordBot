#!/usr/bin/env python3
## Tokens, api keys, and secrets should be kept in keys.txt and read by keys.read
## keys.txt
##  | Discord: <Discord token>

def read(*IDs, file="keys.txt"):
    with open(file) as keysFile:
        keysRead = keysFile.read().strip()
    keys = {}
    for key in keysRead.split("\n"):
        keys[key.split(": ")[0].lower()] = key.split(": ")[1]
    if len(IDs) == 1:
        return keys[IDs[0].lower()]
    returnKeys = ()
    for ID in IDs:
        returnKeys += (keys[ID.lower()],)
    return returnKeys
