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
        if 'location' in msg and users['status'] == "Weather" :
            self.latitude = str(msg['location']['latitude'])
            self.longitude = str(msg['location']['longitude'])  
            self.isCall =True          
            return True
#            'location': {'latitude': 25.043579, 'longitude': 121.534496}
        elif 'text' in msg and msg['text'] == '/weather':
            users['status'] = "Weather"
            return True 
        else:
            return False
   
    def main(self, users, msg):
        bot = self.bot
        content_type, chat_type, chat_id = telepot.glance(msg)
        if self.isCall:
            bot.sendMessage(chat_id, "請等等...")
            a = WeatherCrawler(self.latitude, self.longitude)
            bot.sendMessage(chat_id, a.getInfo())
            self.isCall = False
            a = None
            users["status"] = None
            print("send message")
        else:
            self.callWeather(users, msg)
            
        print("SampleTask worked!")
        
    def callWeather(self,users, msg):
            bot = self.bot
            content_type, chat_type, chat_id = telepot.glance(msg)
            bot.sendMessage(chat_id, '請給我您現在的位置',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="送出位置",request_location=True),
                                    KeyboardButton(text="送出電話",request_contact=True)]
                                ]
                            ))
    