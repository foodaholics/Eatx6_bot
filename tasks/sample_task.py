#!/usr/bin/env python3

import telepot

from tasks.base_task import BaseTask

class SampleTask(BaseTask):
    def trig(self, user, msg):
        return msg['text'] == '/test'

    def main(self, user, msg):
        bot = self.bot


        bot.sendMessage(user['chat_id'], msg['text'])
        print("SampleTask worked!")