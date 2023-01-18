#!/usr/bin/env python3
__author__ = "Joe Baker (JoeBlakeB)"
__copyright__ = "Copyright 2023, Joe Baker (JoeBlakeB)"
__credits__ = ["JoeBlakeB"]
__license__ = "GPL"

import os
import sys

class Config:
    def __init__(self):
        if "--config" in sys.argv:
            if len(sys.argv) > sys.argv.index("--config") + 1:
                self.dir = sys.argv[sys.argv.index("--config") + 1]
            else:
                raise ValueError("No config directory specified")
        else:
            self.dir = "config/"
        os.makedirs(self.dir, exist_ok=True)
        