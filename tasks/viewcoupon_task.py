#!/usr/bin/env python3

import telepot

from tasks.base_task import BaseTask

class ViewCouponTask(BaseTask):
    def trig(self, users, msg):
        # 把 self.bot 簡寫成 bot
        bot = self.bot

        # 取得使用者的資訊
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')


        # TODO: 判斷是否觸發
        result = 'text' in msg and msg['text'] in ['/viewcoupon']


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
        bot.sendMessage(chat_id, "查看折價券的功能建置中！")
        print("[ViewCouponTask] main")