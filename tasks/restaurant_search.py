
from time import *
from pprint import pprint

import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from datetime import *
from tasks.base_task import BaseTask

class RestaurantSearch(BaseTask):
    def __init__(self, bot: telepot.Bot):
        super().__init__(bot)
        self.key = 'AIzaSyB2R2Xlp4rAQZb6hDd22wcBuHnV1061BDA'
        self.location = '25.043387,121.535046'
        self.session_request = requests.session()
        self.message_id = None
    
    # 取得地點的詳細資訊 -- 預設取得： 地址、名稱、評價、電話、營業時間
    def place_details(self, placeid='', fields='formatted_address,name,rating,formatted_phone_number,opening_hours', language='zh-TW', key=None):
        if key == None:
            key = self.key
        url = 'https://maps.googleapis.com/maps/api/place/details/json?' + \
            'placeid=' + placeid + '&' \
            'fields=' + fields + '&' + \
            'language=' + language + '&' + \
            'key=' + key
        return self.session_request.get(url).json()['result']

    # 搜尋半徑 500 公尺 內的餐廳(預設)
    def near_by_search(self, output='json?', location=None, radius='500', pleace_type='restaurant', language='zh-TW', key=None):
        if key == None:
            key = self.key
        if location == None:
            location = self.location
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/' + output + \
            'location=' + location + '&' + \
            'radius=' + radius + '&' + \
            '&type=' + pleace_type + '&' + \
            '&language=' + language + '&' + \
            '&key=' + key
        return self.session_request.get(url).json()['results']

    def get_store_names_and_placeIDs(self, data:dict):
        # places_result = self.near_by_search()
        tmp = {}
        for i in data:
            place_id = i['place_id']
            tmp[place_id] = self.place_details(place_id)['name']
        return tmp
            

    def get_infomation(self, place_id=None):
        if place_id == None:
            return '可以先給我 place_id ?'
        details = self.place_details(place_id)
        result = ''
        mpaUrl = 'https://www.google.com/maps/search/?api=1&query=' + details['name'] + '&query_place_id=' + place_id
        if 'name' in details:
            result += '店名: ' + details['name'] + '\n'
        if 'formatted_address' in details:
            result += '地址: ' + details['formatted_address'] + '\n'
        if 'formatted_phone_number' in details:
            result += '電話號碼: ' + details['formatted_phone_number'] + '\n'
        if 'opening_hours' in details:
            result += '營業時間: ' + details['opening_hours']['weekday_text'][date.today().weekday()] + '\n'
            result += '現在是否營業: ' + str(details['opening_hours']['open_now']) + '\n'
        if 'rating' in details:
            result += '評價: ' + str(details['rating']) + '\n'
        result += '[在地圖上顯示](' + mpaUrl + ')'
        return result
        

    def test(self):
        places_result = self.get_store_names_and_placeIDs()
        tmp = [{i: places_result[i]}for i in places_result]
        self.get_infomation('ChIJs9HOcHypQjQRlMPKm2JfIjw')

    def trig(self, users, msg):
        bot = self.bot

        # 取得使用者的 chat_id        
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

        if 'text' in msg and msg['text'] == '/eat':
            users[chat_id]['status'] = '/eat'
            return True
        elif users[chat_id]['status'] == '/eat' and 'location' in msg:
            return True
        elif users[chat_id]['status'] == '/eat' and 'chat_instance' in msg:
            return True
        else:
            users[chat_id]['status'] = None
            return False
    def main(self, users, msg):
        bot = self.bot
        # 取得使用者的 chat_id
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        if 'text' in msg and msg['text'] == '/eat' and users[chat_id]['status'] == '/eat':
            replyKeyboard = ReplyKeyboardMarkup(keyboard=
            [
                [KeyboardButton(text='送啦', request_location=True)]
            ], 
            resize_keyboard=True, one_time_keyboard=True)
            bot.sendMessage(chat_id, '請把你的位置發送給我 😬', reply_markup=replyKeyboard)         

        elif 'location' in msg and users[chat_id]['status'] == '/eat':
            location = str(msg['location']['latitude']) + ',' + str(msg['location']['longitude'])
            bot.sendMessage(chat_id, '請稍候 😣😣😣')
            places_result = self.get_store_names_and_placeIDs(self.near_by_search(location=location))
            tmp = [{'place_id': i, 'name': places_result[i]}for i in places_result]
            inline_keyboards = []
            start = 0
            end = 3
            for i in range(len(tmp)):
                listTmp = []
                for j in tmp[start:end]:
                    listTmp.append(InlineKeyboardButton(text=j['name'], callback_data=j['place_id']))
                inline_keyboards.append(listTmp)
                start = end
                end += 3
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboards)
            bot.sendMessage(chat_id, '這些是我找到的餐廳列表', reply_markup=replyKeyboard)
            self.message_id = None

        elif 'chat_instance' in msg and users[chat_id]['status'] == '/eat':
            message = self.get_infomation(query_data)
            if self.message_id == None:
                self.message_id = msg['message']['message_id'] + 1
                bot.answerCallbackQuery(query_id)
                bot.sendMessage(chat_id, message, parse_mode='Markdown', disable_web_page_preview=True)
            else:
                bot.answerCallbackQuery(query_id)
                bot.editMessageText((chat_id, self.message_id), message, parse_mode='Markdown', disable_web_page_preview=True)
            # users[chat_id]['status'] = None
        print("[RestaurantSearch] main")