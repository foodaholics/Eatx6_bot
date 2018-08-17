#!/usr/bin/env python3

import telepot

# 作為所有 Task 的父類別，請不要更改這部分的程式碼。

class BaseTask:
    def __init__(self, bot:telepot.Bot):
        self.bot = bot

    def trig(self, users, msg):
        return False

    def main(self, users, msg):
        bot = self.bot