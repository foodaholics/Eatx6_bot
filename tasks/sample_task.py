#!/usr/bin/env python3

import telepot

from tasks.base_task import BaseTask

class SampleTask(BaseTask):
    def trig(self, users, msg):
        bot = self.bot

        # 取得使用者的 chat_id
        content_type, chat_type, chat_id = telepot.glance(msg)
        
        return 'text' in msg and msg['text'] == '/test'

    def main(self, users, msg):
        bot = self.bot

        # 取得使用者的 chat_id
        content_type, chat_type, chat_id = telepot.glance(msg)

        bot.sendMessage(chat_id, msg['text'])
        print("[SampleTask] main")