#!/usr/bin/env python3

import telepot

from modules.base_module import BaseModule

class SampleModule(BaseModule):
    def setup(self):
        # 把 self.bot 簡寫成 bot
        bot = self.bot


        # TODO: 實作模組初始設定
        print("[SampleModule] setup")

    def loop(self):
        # 把 self.bot 簡寫成 bot
        bot = self.bot


        # TODO: 實作模組定時執行的功能
        print("[SampleModule] loop")