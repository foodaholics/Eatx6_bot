#!/usr/bin/env python3

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

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
        result = ('text' in msg and msg['text'] in ['/coupon']) or users[chat_id]['status'] == '/coupon'


        # 回傳是否觸發的結果
        return result

    def main(self, users, msg):
        # 把 self.bot 簡寫成 bot
        bot = self.bot

        print("[ViewCouponTask] main")

        # 取得使用者的資訊
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        # TODO: 實作實際的功能
        if users[chat_id]['status'] != '/coupon':
            # 設定狀態
            users[chat_id]['status'] = '/coupon'

            # 顯示目前有哪些商店支援優惠券
            keyboard = [[]]
            for key in self.data['stores'].keys():
                if len(keyboard[-1]) < 3:
                    keyboard[-1].append(InlineKeyboardButton(text=key, callback_data=key))
                else:
                    keyboard.append([InlineKeyboardButton(text=key, callback_data=key)])

            bot.sendMessage(chat_id, "我目前有這些餐廳的優惠券～你想看看哪一家的？", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        else:
            bot.sendMessage(chat_id, "想看折價券齁？")