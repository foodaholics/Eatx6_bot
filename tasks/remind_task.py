from tasks.base_task import BaseTask
import time
import datetime
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class RemindTask(BaseTask):
    def __init__(self, bot:telepot.Bot):
        super().__init__(bot)
        self.select = {}
        self.status =None
        self.message = None
        self.message_id = None
        self.job = {}
        self.replydic={"select":["要新增提醒還是要顯示已新增的提醒","新增提醒","顯示提醒"],
                        "setting_day":["需要每天都提醒，還是只要提醒幾天就好,還是只要提醒今天就好","今天","每天","輸入n天","返回"],
                        "display":["以下為所有的提醒","xxx提醒","返回"],
                        "setting_day_input":["輸入n天(請輸入一正整數)","取消","上一步"],
                        "setting_start_time":["什麼時候要開始提醒,可以選擇以下按鈕,或輸入日期(2018-01-01)","今天","取消","上一步"],
                        "setting_times":["每天提醒幾次","1次","2次","3次","4次","5次","6次","取消","上一步"],
                        "set_time":["每天幾點提醒,根據您『每天提醒幾次』來輸入n個時間,\n例如：每天提醒2次，每天下午一點及兩點提醒,就輸入 13:00 14:00","取消","上一步"],
                        "input_job_name":["請輸入此提醒名稱及要提醒的文字,例如：吃感冒藥 該吃藥了,帥哥(提醒名稱及提醒文字,中間以空格區隔)"],
                        "finish":["請確認以下內容是否有誤，沒問題請按ok，修改請按上一步","ok","取消","上一步"]
                        }
                        

    def trig(self, users, msg):
        # print("status=",self.status)
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        from_id = msg['from']['id']
        #第一次執行
        if 'text' in msg and msg['text'] == '/remind':
            users[from_id]['status'] = "Remind"
            self.message_id = None
            self.status = "select"
            return True

        elif 'data' in msg and users[from_id]['status']=='Remind' and self.status=="select":
            if msg['data'] == '新增提醒':
                self.status = "setting_day"
            elif msg['data'] == '顯示提醒':
                self.status = "display"
            return True

        elif 'data' in msg and users[from_id]['status']=='Remind' and self.status=="setting_day":
            if msg['data'] == '今天':
                self.select["setting_day"] = 'date'
                self.select['setting_start_time'] = (datetime.datetime.now()).strftime("%Y-%m-%d")
                self.status = 'setting_times'
                return True
            else:
                self.select["setting_day"] = 'interval'
            if msg['data'] == '每天':
                self.status = "setting_start_time"
            elif msg['data'] == '輸入n天':
                self.status = "setting_day_input"
            elif msg['data'] == '返回':
                del self.select['setting_day']
                self.status = "select"
            return True

        elif ('text' in msg or 'data' in msg) and users[from_id]['status']=='Remind' and self.status=="setting_day_input":
            if 'text' in msg:
                self.select['setting_day'] = 'interval'
                self.select['end_day']=msg['text']
            if 'data' in msg and msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif 'data' in msg and msg['data'] == '上一步':
                del self.select['setting_day']
                del self.select['days']
                if 'end_day' in self.select:
                    del self.select['end_day']
                self.status = "setting_day"
            else:
                self.status = "setting_start_time"
            return True
       
        elif  ('text' in msg or 'data' in msg) and users[from_id]['status']=='Remind' and self.status=="setting_start_time":
            if 'text' in msg:
                self.select['setting_start_time'] = msg['text']
            elif 'data' in msg:
                self.select['setting_start_time'] = (datetime.datetime.now()).strftime("%Y-%m-%d")
            if 'data' in msg and msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif 'data' in msg and msg['data'] == '上一步':
                del self.select['setting_start_time']
                self.status = "setting_day"
            else:
                self.status = "setting_times"
            return True
        
        elif 'data' in msg and users[from_id]['status']=='Remind' and self.status=="setting_times":
            self.select['setting_times'] = msg['data'][0]
            if msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif msg['data'] == '上一步':
                del self.select['setting_times']
                self.status = "setting_start_time"
            else:
                self.status = "set_time"
            return True
        
        elif ('text' in msg or 'data' in msg) and users[from_id]['status']=='Remind' and self.status=="set_time":
            if 'text' in msg:
                self.select['set_time'] = msg['text']
            if 'data' in msg and msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif 'data' in msg and msg['data'] == '上一步':
                del self.select['set_time']
                self.status = "setting_times"
            else:
                self.status = "input_job_name"
            return True

        elif  ('text' in msg or 'data' in msg) and users[from_id]['status']=='Remind' and self.status=="input_job_name":
            self.message = None
            if 'text' in msg:
                self.select['input_job_name'] = msg['text']
            if 'data' in msg and msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif 'data' in msg and msg['data'] == '上一步':
                del self.select['input_job_name']
                self.status = "set_time"
            else:
                if 'end_day' in self.select:
                    end_day = int(self.select['end_day'])
                    temp = list(map(int,self.select['setting_start_time'].split('-')))
                    self.select['end_day'] = (datetime.datetime(temp[0],temp[1],temp[2])+ datetime.timedelta(days=end_day)).strftime("%Y-%m-%d")
                self.status = "finish"
                self.message = self.select
                text , name = self.chatMessage(self.message)
                if from_id in self.job:
                    self.job[from_id][name] = text
                else:
                    self.job[from_id] = {name:text}

            return True

        elif  ('text' in msg or 'data' in msg) and users[from_id]['status']=='Remind' and self.status=="finish":
            print(self.select)
            if 'data' in msg and msg['data'] == '取消':
                self.select = {}
                self.status = "select"
            elif 'data' in msg and msg['data'] == '上一步':
                self.status = "input_job_name"
            elif 'data' in msg and msg['data'] == 'ok':
                self.status = "select"
            return True

        elif 'data' in msg and users[from_id]['status']=='Remind' and self.status=="display":
            self.select[msg['message']['text']] = msg['data']
            if msg['data'] == 'xxx提醒':
                self.status = ""
            elif msg['data'] == '返回':
                self.status = "select"
            return True

        else:
            return False
        
    def main(self, users, msg):
        bot = self.bot
        from_id = msg['from']['id']
        # print("[RemindTask] main")
        # print('users',users)
        # print("status=",self.status)
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
        except:
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        keyboard, text = self.creatButton(self.status,self.replydic)
        if self.message != None:
            text , name = self.chatMessage(self.message)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        #讓訊息被覆蓋
        if 'message' in msg and 'message_id' in msg['message']:
                self.message_id = msg['message']['message_id']       
        if self.message_id == None:
            bot.sendMessage(from_id, text, parse_mode='Markdown',reply_markup= keyboard, disable_web_page_preview=True)

        elif 'text' in msg:
            self.message_id = msg['message_id'] + 1
            bot.sendMessage(from_id, text,reply_markup= keyboard)
        else:
            bot.editMessageText((from_id, self.message_id), text, parse_mode='Markdown',reply_markup= keyboard, disable_web_page_preview=True)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # bot.sendMessage(from_id, text,reply_markup= keyboard)
        if self.message != None:
            self.message = None
      
    def creatButton(self, status, dic):
        button = []
        index = 0
        for status in self.replydic.keys():
            if status == self.status:
                text = self.replydic[status][0]
                if len(self.replydic[status][1:]) > 3:
                    for _ in range(0,len(self.replydic[status][1:]),3):
                        button.append([])
                if len(button) >= 1:
                    count = 0
                    for output in self.replydic[status][1:] :
                        button[index].append(InlineKeyboardButton( text=output, callback_data=output))
                        if count < 2:
                            count += 1
                        else:
                            count = 0
                            index += 1
                    keyboard = InlineKeyboardMarkup(inline_keyboard= button)
                    break
                else:
                    for output in self.replydic[status][1:] :
                        button.append(InlineKeyboardButton( text=output, callback_data=output))
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[button])
                    break
        return keyboard ,text

    def chatMessage(self,message):
        # 您設定”setting_start_time”開始提醒，於”end_day”結束提醒，每天提醒”setting_times”次，每天”set_time”提醒
        # 您將這個提醒名稱命名為”input_job_name”，提醒文字為”input_job_name”
        # print('message' , message)
        name , text = message['input_job_name'].split()
        if 'end_day' in message:
            string = "您設定 " + (message['setting_start_time']) + " 開始提醒\n於 " + str(message['end_day']) + "結束提醒\n每天提醒 " + str(message['setting_times']) + " 次\n每天 " + str(message['set_time']) + " 提醒\n您將這個提醒名稱命名為：" + str(name) + "\n提醒文字為：" + str(text)
        elif message['setting_day'] == 'date':
            string = "您設定 " + str(message['setting_start_time']) + " 開始提醒\n今天提醒 " + str(message['setting_times']) + " 次\n今天 " + str(message['set_time']) + " 提醒\n您將這個提醒名稱命名為：" + str(name) + "\n提醒文字為：" + str(text)
        else:
            string = "您設定 " + str(message['setting_start_time']) + " 開始提醒\n每天提醒 " + str(message['setting_times']) + " 次\n每天 " + str(message['set_time']) + " 提醒\n您將這個提醒名稱命名為：" + str(name) + "\n提醒文字為：" + str(text)
        return string ,name


