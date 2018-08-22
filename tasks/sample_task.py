#!/usr/bin/env python3

import telepot

from tasks.base_task import BaseTask

class SampleTask(BaseTask):
    def trig(self, users, msg):
        # 把 self.bot 簡寫成 bot
        bot = self.bot

        # 取得使用者的資訊
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')


        # TODO: 判斷是否觸發
        result = 'text' in msg and msg['text'] in ['/start', '/help']


        # 回傳是否觸發的結果
        return result

    def main(self, users, msg):
        # 把 self.bot 簡寫成 bot
        bot = self.bot

        # 取得使用者的資訊
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        # TODO: 實作實際的功能
        bot.sendMessage(chat_id, "/help - 我需要幫助☺️\n/start - 讓我們從新開始吧!❤️\n/eat - 找吃的，如果你不想思考附近可以吃什麼🤤\n/remind - 為忘東忘西吃貨設計的提醒🤔\n/weather - 查天氣，畢竟吃貨出門是需要看天氣的😇\n/coupon - 查看窮窮的吃貨最需要的折價卷😆\n/subscribe - 訂閱折價卷🤣\n/unsubscribe - 取消訂閱折價卷😫")
        print("[SampleTask] main")