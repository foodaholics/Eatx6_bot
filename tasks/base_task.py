#!/usr/bin/env python3

import telepot

class BaseTask:
    def __init__(self, bot:telepot.Bot):
        self.bot = bot

    def trig(self, user, msg):
        return False

    def main(self, user, msg):
        bot = self.bot