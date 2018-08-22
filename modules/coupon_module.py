#!/usr/bin/env python3

import telepot
from modules.base_module import BaseModule
import schedule
from modules.BKSpider import BKSpider
from modules.KFCSpider import KFCSpider
from modules.MosSpider import MosSpider
from modules.McDSpider import McDSpider
from modules.twentyOneCenturySpider import twentyOneCenturySpider
from modules.TKKSpider import TKKSpider
from modules.ticket import Ticket

class CouponModule(BaseModule):
    def __init__(self,bot,data:dict):
        super().__init__(bot,data)
        
        self.tickets = Ticket()

    # 取得新coupon與即將到期coupon
    def update(self):
        print("UPDATE")
        for restaurant in self.data["stores"].values():
            # 拿各家店裡的新coupon
            restaurant["newKeys"] = self.tickets.getNewCoupon(restaurant["oldData"],restaurant["coupons"])
            # 拿各家店裡即將到期的coupon
            restaurant["lastDayKeys"] = self.tickets.getLastDayCoupon(restaurant["coupons"])

    # 傳送照片   
    def botSendPhoto(self,bot,couponImg,ID):
        for img in couponImg:
            bot.sendPhoto(ID,img)

    # 跑迴圈來發送給每一個訂閱者
    def notify(self):
        print("NODIFY")
        bot = self.bot
        
        for restaurant in self.data["stores"].values(): # 跑各個店家
            for ID in restaurant["subscribers"]: # 跑各個訂閱者
                if len(restaurant["newKeys"]) != 0: # 有新的coupon，傳送給訂閱者
                    for key in restaurant["newKeys"]:
                        bot.sendMessage(ID,self.tickets.printCoupon(key,restaurant["coupons"]))
                        self.botSendPhoto(bot,restaurant["coupons"][key]["img"],ID)
                if len(restaurant["lastDayKeys"]) != 0: 
                    for key in restaurant["lastDayKeys"]: # 有即將到期的coupon，傳送給訂閱者 
                        bot.sendMessage(ID,self.tickets.printCoupon(key,restaurant["coupons"]))
                        self.botSendPhoto(bot,restaurant["coupons"][key]["img"],ID)


    # 執行update跟notify，處理完後把今天抓的資料放進oldData
    def execute(self):
        print("[CouponModule] execute")
        for restaurant,info in self.data["stores"].items(): # 爬一次當天的新資料
            info["coupons"] = self.data["stores"][restaurant]["spider"].get_coupons()
        self.update()
        self.notify() 
        for restaurant in self.data["stores"].values(): # 執行完 update 跟 notify 之後把當天新資料放入old data
            restaurant["oldData"] = restaurant["coupons"]

    def setup(self):
        stores = {"肯德基":{"subscribers":[],
                "spider":KFCSpider(),
                "coupons":{},
                "newKeys":[],
                "lastDayKeys":[],
                "oldData":{}},
        "漢堡王":{"subscribers":[],
            "spider":BKSpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}},
        "摩斯漢堡":{"subscribers":[],
            "spider":MosSpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}},
        "麥當勞":{"subscribers":[],
            "spider":McDSpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}},
        "21世紀":{"subscribers":[],
            "spider":twentyOneCenturySpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}},
        "頂呱呱":{"subscribers":[],
            "spider":TKKSpider(),
            "coupons":{},
            "newKeys":[],
            "lastDayKeys":[],
            "oldData":{}}
        }
        self.data["stores"] = stores

        # note:測試時schedule設定的時間要在下面爬蟲都結束之後開始，否則會跟execute裡面的爬蟲衝突
        '''
        for restaurant,info in self.data["stores"].items(): # setup先抓一次資料
            info["coupons"] = self.data["stores"][restaurant]["spider"].get_coupons()
            print("restaurant",restaurant,info)
        '''
        print("[CouponModule] setup")
        schedule.every().day.at("15:58").do(self.execute)
        #schedule.every(10).minutes.do(self.execute)

        self.execute()
                
    def loop(self):
        bot = self.bot
        schedule.run_pending()
        print("[CouponModule] loop")