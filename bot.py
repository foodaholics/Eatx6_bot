#!/usr/bin/env python3

import sys
import time
import json
from pprint import pprint

import telepot
from telepot.loop import MessageLoop

from tasks.weather_task import WeatherTask
from tasks.sample_task import SampleTask
from modules.sample_module import SampleModule

# 載入設定值
with open(sys.path[0] + '/config.json', 'r') as f:
    config = json.load(f)
# 取得 bot 控制權
bot = telepot.Bot(config['TOKEN'])

# 載入功能
tasks = [SampleTask(bot),WeatherTask(bot)]
# 載入模組
modules = [SampleModule(bot)]

# 存放使用者的資料
users = {}

def on_chat(msg):
    # 除錯訊息
    pprint(msg)

    # 取得使用者的資訊
    content_type, chat_type, chat_id = telepot.glance(msg)
    from_id = msg['from']['id']
        
    # 有新的使用者就新增到 users 裡
    if not from_id in users:
        users[from_id] = {
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
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

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

    for module in modules:
        module.setup()

    while True:
        for module in modules:
            module.loop()
        time.sleep(10)

if __name__ == '__main__':
    main()