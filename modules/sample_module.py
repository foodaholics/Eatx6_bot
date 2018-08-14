#!/usr/bin/env python3

import telepot

from modules.base_module import BaseModule

class SampleModule(BaseModule):
    def setup(self):
        bot = self.bot

        print("[SampleModule] setup")

    def loop(self):
        bot = self.bot

        print("[SampleModule] loop")