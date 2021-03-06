#!/usr/bin/env python3

import telepot
from telepot.namedtuple import KeyboardButton,ReplyKeyboardMarkup
from tasks.base_task import BaseTask
from tasks.weather_crawler import WeatherCrawler
class WeatherTask(BaseTask):
    def __init__(self, bot:telepot.Bot):
        super().__init__(bot)
        self.latitude = ""
        self.longitude = ""
        self.isCall = False
        
    def trig(self, users, msg):
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        if 'location' in msg and users[chat_id]['status'] == "Weather" :
            self.latitude = str(msg['location']['latitude'])
            self.longitude = str(msg['location']['longitude'])  
            self.isCall =True
            return True
#            'location': {'latitude': 25.043579, 'longitude': 121.534496}
        elif 'text' in msg and msg['text'] == '/weather':
            users[chat_id]['status'] = "Weather"
            return True 
        else:
            return False
   
    def main(self, users, msg):
        bot = self.bot

        print("[WeatherTask] main")

        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        if self.isCall:
            bot.sendMessage(chat_id, "請稍候 😣😣😣")
            a = WeatherCrawler(self.latitude, self.longitude)
            bot.sendMessage(chat_id, a.getInfo())
            self.isCall = False
            a = None
            users[chat_id]["status"] = None
            # print("send message")
        else:
            self.callWeather(users, msg)
        # print(users)
            
        # print("SampleTask worked!")
        
    def callWeather(self,users, msg):
            bot = self.bot
            content_type, chat_type, chat_id = telepot.glance(msg)
            bot.sendMessage(chat_id, '請把你的位置發送給我 😬',
                            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True,
                                keyboard=[
                                    [KeyboardButton(text="送啦",request_location=True)]
                                ]
                            ))
    