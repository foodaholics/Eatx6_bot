#!/usr/bin/env python3

import telepot

from tasks.base_task import BaseTask

class SampleTask(BaseTask):
    def trig(self, users, msg):
        bot = self.bot

        # 取得使用者的 chat_id
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        return 'text' in msg and msg['text'] in ['/start', '/help']

    def main(self, users, msg):
        bot = self.bot

        # 取得使用者的 chat_id
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        bot.sendMessage(chat_id, "我現在可以幫你( ºωº )\n\n/weather - 查天氣，畢竟吃貨出門是需要看天氣的😇\n/eat - 找吃的，如果你不想思考附近可以吃什麼🤤")
        print("[SampleTask] main")