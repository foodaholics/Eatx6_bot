#!/usr/bin/env python3

import telepot

class BaseModule:
    def __init__(self, bot:telepot.Bot):
        self.bot = bot

    def setup(self):
        bot = self.bot

    def loop(self):
        bot = self.bot