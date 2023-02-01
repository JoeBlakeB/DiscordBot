#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import json
import os
import sys

class Config:
    filename = "servers.json"
    data = {}
    defaults = {
        "messageCommandsEnabled": True,
        "prefix": "!"
    }

    def __init__(self):
        if "--config" in sys.argv:
            if len(sys.argv) > sys.argv.index("--config") + 1:
                self.dir = sys.argv[sys.argv.index("--config") + 1]
            else:
                raise ValueError("No config directory specified")
        else:
            self.dir = "config/"
        os.makedirs(self.dir, exist_ok=True)

        self.filepath = os.path.join(self.dir, self.filename)
        
        try:
            with open(self.filepath) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            pass
    
    def __getitem__(self, key):
        """Get a config value for a server.
        
        Arguments:
        key -- The path to the config value to get [serverID] or [serverID, key]
        Returns:
        The config value if key specified, otherwise a ServerConfig object
        """
        serverID = str(key) if type(key) != tuple else str(key[0])
        if serverID not in self.data:
            data = self.defaults
        else:
            data = {
                **self.defaults,
                **self.data[serverID]
            }

        if type(key) == tuple:
            return data[key[1]]
        return ServerConfig(self, serverID, data)

    def __setitem__(self, key, value):
        """Set a config value for a server and save it to the config file.
        
        Parameters:
            key (string or int (serverID) or tuple (serverID, key))
                The path to the config value to set
            value (any)
                The value to set the config value to
        """
        if type(value) == ServerConfig:
            value = value.config

        if type(key) == str:
            self.data[key] = value
        elif type(key) == tuple:
            if key[0] not in self.data:
                self.data[key[0]] = {}
            self.data[key[0]][key[1]] = value
        
        with open(os.path.join(self.dir, self.filename), "w") as f:
            json.dump(self.data, f, indent=4)


class ConfigCustomDefaults(Config):
    def __init__(self, defaults={}, filename="config.json"):
        """Create a new config object with custom defaults.
        
        Parameters:
            defaults (dict) (optional: {})
                The default config values
            filename (string) (optional: "config.json")
                The name of the config file
        """
        self.defaults = defaults
        self.filename = filename
        super().__init__()
    

class ServerConfig:
    allConfig = None
    config = {}
    serverID = None

    def __init__(self, allConfig, serverID, config):
        self.allConfig = allConfig
        self.serverID = serverID
        self.config = config

    def __getitem__(self, key):
        """Get a config value."""
        return self.config[key]

    def __setitem__(self, key, value):
        """Set a config value for a server and save it to the config file."""
        self.config[key] = value
        self.allConfig[self.serverID, key] = value
