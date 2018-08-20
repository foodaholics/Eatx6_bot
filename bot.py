#!/usr/bin/env python3

import sys
import time
import json
from pprint import pprint

import telepot
from telepot.loop import MessageLoop

from tasks.weather_task import WeatherTask
from tasks.sample_task import SampleTask
from tasks.restaurant_task import RestaurantTask
from modules.sample_module import SampleModule
from modules.coupon_module import CouponModule

# 載入設定值
with open(sys.path[0] + '/config.json', 'r') as f:
    config = json.load(f)
# 取得 bot 控制權
bot = telepot.Bot(config['BOT_TOKEN'])

# 存放使用者的資料
users = {}
# 功能與模組間的全域變數
data = {}

# 載入功能
tasks = [SampleTask(bot), WeatherTask(bot), RestaurantTask(bot, config['PLACE_KEY'])]
# 載入模組
modules = [SampleModule(bot), CouponModule(bot,data)]


def on_chat(msg):
    # 除錯訊息
    pprint(msg)

    # 取得使用者的資訊
    content_type, chat_type, chat_id = telepot.glance(msg)
        
    # 有新的使用者就新增到 users 裡
    if not chat_id in users:
        users[chat_id] = {
            'status': None
        }

    # 嘗試觸發每個功能
    for task in tasks:
        if task.trig(users, msg):
            task.main(users, msg)
            break

def on_callback_query(msg):
    # 除錯訊息
    pprint(msg)

    # 取得使用者的 from_id
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

    # 嘗試觸發每個功能
    for task in tasks:
        if task.trig(users, msg):
            task.main(users, msg)
            break

def main():
    # 接收使用者對 bot 的輸入並以相關函式處理
    MessageLoop(bot, {
        'chat': on_chat,
        'callback_query': on_callback_query
    }).run_as_thread()

    print("我開始運作啦！")

    # 執行模組的 setup()
    for module in modules:
        module.setup()

    # 每隔 10 秒觸發模組的 loop()
    while True:
        for module in modules:
            module.loop()
        time.sleep(10)

if __name__ == '__main__':
    main()