#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import json
import os
import warnings

class Secrets:
    def __init__(self, config):
        self.config = config
        try:
            with open(os.path.join(self.config.dir, "secrets.json")) as f:
                self.secrets = json.load(f)
        except FileNotFoundError:
            self.secrets = {}
            self.add("discord")
            raise FileNotFoundError("Please add your tokens to secrets.json")

    def add(self, key):
        self.secrets[key] = ""
        with open(os.path.join(self.config.dir, "secrets.json"), "w") as f:
            json.dump(self.secrets, f, indent=4)

    def get(self, key, default=None):
        try:
            value = self.secrets[key]
        except KeyError:
            self.add(key)
            value = default
        if not value:
            warnings.warn(f"The secrets.json file does not contain a value for '{key}'", Warning)
        return value
