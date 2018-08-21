#!/usr/bin/env python3

from datetime import date

import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from tasks.base_task import BaseTask
class SubscribeTask(BaseTask):
    def __init__(self, bot:telepot.Bot, data:dict):
        super().__init__(bot, data)

    def trig(self, users, msg):
        bot = self.bot

        # 取得使用者的 from_id
        from_id = msg['from']['id']
        # 取得使用者的 chat_id
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        if 'text' in msg and msg['text'] == '/subscribe':
            users[chat_id]['status'] = '/subscribe'
            return True
        elif 'text' in msg and msg['text'] == '/unsubscribe':
            users[chat_id]['status'] = '/unsubscribe'
            return True    
        elif users[chat_id]['status'] in ['/subscribe', '/unsubscribe'] and 'chat_instance' in msg:
            return True        
        elif 'text' in msg and msg['text'] != '/subscribe' and users[chat_id]['status'] == '/subscribe':
            return False
        # return False

    def main(self, users, msg):
        bot = self.bot
        
        # 取得使用者的 from_id
        from_id = msg['from']['id']
        # 取得使用者的 chat_id
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        if 'text' in msg and msg['text'] == '/subscribe' and users[chat_id]['status'] == '/subscribe':
            inline_keyboards = []
            for i in self.data['stores']:
                inline_keyboards.append([InlineKeyboardButton(text=i, callback_data=i)])
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)
            bot.sendMessage(chat_id, '你要訂閱甚麼折價券呀', reply_markup=replyKeyboard)

        elif 'text' in msg and msg['text'] == '/unsubscribe' and users[chat_id]['status'] == '/unsubscribe':
            inline_keyboards = []
            for i in self.data['stores']:
                if chat_id in self.data['stores'][i]['subscribers']:
                    inline_keyboards.append([InlineKeyboardButton(text=i, callback_data=i)])
            if len(inline_keyboards):
                replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)
                bot.sendMessage(chat_id, '點你要取消訂閱的折價券', reply_markup=replyKeyboard)
            else:
                bot.sendMessage(chat_id, '你還沒訂閱拉')
                users[chat_id]['status'] = None 

        elif 'chat_instance' in msg and users[chat_id]['status'] == '/subscribe':
            bot.answerCallbackQuery(query_id)
            if chat_id not in self.data['stores'][query_data]['subscribers']:
                self.data['stores'][query_data]['subscribers'].append(chat_id)
                bot.editMessageText((chat_id, msg['message']['message_id']), query_data + '：訂閱成功！')
            else:
                bot.editMessageText((chat_id, msg['message']['message_id']), query_data + '：你已經訂閱過囉！')
            users[chat_id]['status'] = None        
            print(self.data['stores'])

        elif 'chat_instance' in msg and users[chat_id]['status'] == '/unsubscribe':
            bot.answerCallbackQuery(query_id)
            self.data['stores'][query_data]['subscribers'].remove(chat_id)
            bot.editMessageText((chat_id, msg['message']['message_id']), query_data + '取消成功！')
            users[chat_id]['status'] = None        
            print(self.data['stores'])
        print("[SubscribersTask] main")