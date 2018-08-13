#!/usr/bin/env python3

import time
from pprint import pprint

import telepot
from telepot.loop import MessageLoop

from config import TOKEN
from tasks.sample_task import SampleTask

# 存放使用者的資料
users = {}

# 取得 bot 控制權
bot = telepot.Bot(TOKEN)

# 載入功能
tasks = [SampleTask(bot)]

def on_chat(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    pprint(msg)

    # 有新的使用者就新增到 users 裡
    if not chat_id in users:
        users[chat_id] = {'chat_id': chat_id}

    # 嘗試觸發每個功能
    for task in tasks:
        if task.trig(users[chat_id], msg):
            task.main(users[chat_id], msg)
            break

# 接收使用者對 bot 的輸入並以 on_chat 函式處理
MessageLoop(bot, on_chat).run_as_thread()

print("我開始運作啦！")

# 不要讓 Bot 直接結束
while True:
    time.sleep(10)