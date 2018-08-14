#!/usr/bin/env python3

import telepot

class BaseTask:
    def __init__(self, bot:telepot.Bot):
        self.bot = bot

    def trig(self, users, msg):
        return False

    def main(self, users, msg):
        bot = self.bot