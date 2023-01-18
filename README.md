# JoeBot for Discord

[![Server](https://shields.io/badge/Server-purple?style=for-the-badge)](https://discord.gg/u3fPjukbq2)
[![Invite](https://shields.io/badge/Invite-blue?style=for-the-badge)](https://discord.com/api/oauth2/authorize?client_id=796433833296658442&permissions=117824&scope=bot)

JoeBotV3 is currently being developed meaning that the invite link adds the old version of JoeBot which doesnt have slash commands. 

JoeBot is a DiscordBot which uses [PyCord](https://github.com/Pycord-Development/pycord) and can be used for multiple things including getting reddit posts with support for text based commands and slash commands.    

## Usage

Python 3.10 and the modules listed in `requirements.txt` are required to run the bot. To install them all, run `python3 -m pip install -r requirements.txt`

The passwords and other logins should be stored in `secrets.json` in the config directory. If it doesn't exist it will be created for the details to be added.

To start the bot, run `./JoeBot.py` or `python3 JoeBot.py`

The config directory will be in the same directory as the bot by default but can be specified with the `--config` argument: `./JoeBot.py --config /path/to/config`
