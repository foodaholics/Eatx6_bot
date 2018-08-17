#!/usr/bin/env python3

import telepot
from modules.base_module import BaseModule
import schedule
from modules.BKSpider import BKSpider
from modules.KFCSpider import KFCSpider
from modules.ticket import Ticket

class CouponModule(BaseModule):
    def __init__(self,bot):
        super().__init__(bot)
        
        self.tickets = Ticket()
        self.KFCOldData = {}
        self.BKOldData = {}
        self.KFCCoupons = None
        self.BKCoupons = None

        self.KFCnewKeys = None
        self.KFClastDayCoupons = None
        self.BKnewKeys = None
        self.BKlastDayCoupons = None

        self.subscribers = {"KFC":["466175780","648984791"],"BK":["466175780","648984791"]}

    def update(self):
        self.KFCnewKeys = self.tickets.getNewCoupon(self.KFCOldData,self.KFCCoupons)
        self.KFClastDayCoupons = self.tickets.getLastDayCoupon(self.KFCCoupons)
        self.BKnewKeys = self.tickets.getNewCoupon(self.BKOldData,self.BKCoupons)
        self.BKlastDayCoupons = self.tickets.getLastDayCoupon(self.BKCoupons)

    def botSendPhoto(self,bot,couponImg,ID):
        for img in couponImg:
            bot.sendPhoto(ID,img)

    def notify(self,subscribers):
        bot = self.bot
        for ID in subscribers["KFC"]:
            if len(self.KFCnewKeys) != 0:
                for key in self.KFCnewKeys:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,self.KFCCoupons))
                    #bot.sendPhoto(ID,self.KFCCoupons[key]["img"])
                    self.botSendPhoto(bot,self.KFCCoupons[key]["img"],ID)

            if len(self.KFClastDayCoupons) != 0:
                for key in self.KFClastDayCoupons:
                    bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,self.KFCCoupons))
                    #bot.sendPhoto(ID,self.KFCCoupons[key]["img"])
                    self.botSendPhoto(bot,self.KFCCoupons[key]["img"],ID)
        for ID in subscribers["BK"]:
            if len(self.BKnewKeys) != 0:
                for key in self.BKnewKeys:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,self.BKCoupons))
                    #bot.sendPhoto(ID,self.BKCoupons[key]["img"])
                    self.botSendPhoto(bot,self.BKCoupons[key]["img"],ID)
            if len(self.BKlastDayCoupons) != 0:
                for key in self.BKlastDayCoupons:
                    bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,self.BKCoupons))
                    #bot.sendPhoto(ID,self.BKCoupons[key]["img"])
                    self.botSendPhoto(bot,self.BKCoupons[key]["img"],ID)

    def execute(self,subscribers):
        self.update()
        self.notify(subscribers) 
        self.KFCOldData = self.KFCCoupons
        self.BKOldData = self.BKCoupons

    def setup(self):
        self.KFCCoupons = KFCSpider().get_coupons()
        self.BKCoupons = BKSpider().get_coupons()    
        print("[CouponModule] setup")
        schedule.every().day.at("10:22").do(self.execute,self.subscribers)
        #schedule.every().day.at("10:15").do(self.execute,self.subscribers)
        
    
        


    def loop(self):
        bot = self.bot
        schedule.run_pending()
        print("[CouponModule] loop")