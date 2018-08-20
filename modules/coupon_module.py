#!/usr/bin/env python3

import telepot
from modules.base_module import BaseModule
import schedule
from modules.BKSpider import BKSpider
from modules.KFCSpider import KFCSpider
from modules.ticket import Ticket

class CouponModule(BaseModule):
    def __init__(self,bot,data:dict):
        super().__init__(bot,data)
        
        self.tickets = Ticket()

    # 取得新coupon與即將到期coupon
    def update(self):
        print("UPDATE")
        KFC = self.data["stores"]["KFC"]
        BK = self.data["stores"]["BK"]
        KFC["newKeys"] = self.tickets.getNewCoupon(KFC["oldData"],KFC["coupons"])
        KFC["lastDayKeys"] = self.tickets.getLastDayCoupon(KFC["coupons"])
        BK["newKeys"] = self.tickets.getNewCoupon(BK["oldData"],BK["coupons"])
        BK["lastDayKeys"] = self.tickets.getLastDayCoupon(BK["coupons"])

    # 傳送照片   
    def botSendPhoto(self,bot,couponImg,ID):
        for img in couponImg:
            bot.sendPhoto(ID,img)

    #跑迴圈來發送給每一個訂閱者
    def notify(self):
        print("NODIFY")
        bot = self.bot
        KFC = self.data["stores"]["KFC"]
        BK = self.data["stores"]["BK"]
        
        for ID in KFC["subscribers"]:
            if len(KFC["newKeys"]) != 0:
                for key in KFC["newKeys"]:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,KFC["coupons"]))
                    self.botSendPhoto(bot,KFC["coupons"][key]["img"],ID)
        
            if len(KFC["lastDayKeys"]) != 0:
                for key in KFC["lastDayKeys"]:
                    bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,KFC["coupons"]))
                    self.botSendPhoto(bot,KFC["coupons"][key]["img"],ID)
        for ID in BK["subscribers"]:
            if len(BK["newKeys"]) != 0:
                for key in BK["newKeys"]:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,BK["coupons"]))
                    self.botSendPhoto(bot,BK["coupons"][key]["img"],ID)
                    if len(BK["lastDayKeys"]) != 0:
                        for key in BK["lastDayKeys"]:
                            bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,BK["coupons"]))
                            self.botSendPhoto(bot,BK["coupons"][key]["img"],ID)

    # 執行update跟notify，處理完後把今天抓的資料放進oldData
    def execute(self):
        stores = self.data["stores"]
        stores["KFC"]["coupons"] = self.data["stores"]["KFC"]["spider"].get_coupons()
        stores["BK"]["coupons"] = self.data["stores"]["BK"]["spider"].get_coupons()
        self.update()
        self.notify() 
        self.data["stores"]["KFC"]["oldData"] = self.data["stores"]["KFC"]["coupons"]
        self.data["stores"]["BK"]["oldData"] = self.data["stores"]["BK"]["coupons"]
        #print("BK old data",self.data["stores"]["BK"]["oldData"])
        print("execute")

    def setup(self):
        
        stores = {"KFC":{"subscribers":["466175780","648984791"],
                "spider":KFCSpider(),
                "coupons":{},
                "newKeys":[],
                "lastDayKeys":[],
                "oldData":{}},
        "BK":{"subscribers":["466175780","648984791"],
            "spider":BKSpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}}
        }
        self.data["stores"] = stores
        
        stores["KFC"]["coupons"] = self.data["stores"]["KFC"]["spider"].get_coupons()
        stores["BK"]["coupons"] = self.data["stores"]["BK"]["spider"].get_coupons()
        #print("BK old data",self.data["stores"]["BK"]["oldData"])

        print("[CouponModule] setup")
        schedule.every().day.at("16:40").do(self.execute)
        #schedule.every(2).minutes.do(self.execute)
                
    def loop(self):
        bot = self.bot
        schedule.run_pending()
        print("[CouponModule] loop")