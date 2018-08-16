#!/usr/bin/env python3

import telepot

# 作為所有 Module 的父類別，請不要更改這部分的程式碼。

class BaseModule:
    def __init__(self, bot:telepot.Bot):
        self.bot = bot

    def setup(self):
        bot = self.bot

    def loop(self):
        bot = self.bot