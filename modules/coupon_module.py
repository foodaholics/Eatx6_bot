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
        self.KFCOldData = {'肯德基暑期宵夜限定優惠 買8塊上校雞塊送香酥脆薯':{'desc' :'即日起至2018/8/27，晚間9:00後至餐廳打烊間， 暑期宵夜限定優惠\n買8塊上校雞塊送香酥脆薯(中)\n限餐廳內用、外帶使用，不適用電話外送、網路訂餐與自助點餐機\n晚間9:00後至餐廳打烊間，至肯德基購買才有優惠喔\n期間限定優惠，只到2018/8/27\n區域: 全台 優惠日期: 2018-08-03 ~ 2018-08-27', 'img':'https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png', 'startDate':'2018-08-03', 'endDate':'2018-08-27'},
                        '肯德基 芒果莎莎咔啦雞腿堡7/31新上市 嘗鮮優惠券 ':{'desc':'肯德基芒果莎莎咔啦雞腿堡7/31新上市\n經典咔啦雞腿排，淋上融合鮮甜芒果泥的清爽莎莎醬，\n再夾入墨西哥脆餅，爽脆萵苣， 蓋上鬆軟芝麻麵包！\n多層次的豐富口感，\n示嘗鮮優惠券， 品嘗夏季限定的美味\n嚐鮮期間：2018/7/31~ 2018/8/27。\n優惠區域: 全台 優惠日期: 2018-07-31 ~ 2018-08-27', 'img':'https://s3.goodlife.tw/system/att/000/017/851/image/1532991351.jpg', 'startDate':'2018-07-31', 'endDate':'2018-08-27'},
                        '肯德基 GoodLife 爸氣雙饗餐 限時優惠券':{'desc':'GoodLife粉絲團 爸氣雙饗餐 18261 1個咔啦脆雞堡+2塊咔啦脆雞+1份勁爆雞米花(大)+1份點心盒(上校雞塊+香酥脆薯)+2顆原味蛋撻+2杯百事可樂(小(原價386元))=NT$249 2018/7/22~2018/9/30\n注意事項: 1.本券可至全國肯德基餐廳使用(台北車站及宜蘭家樂福餐廳不適用)，結帳時出示優惠券(或手機圖檔)， 使用紙券使用後需回收。。 2.限正餐時段(10:30AM起供應)使用，使用期限：2018/7/22~2018/9/30(中秋連假9/22~9/24不適用)，優惠代碼18261。 3.本券不適用外送及網路訂餐，優惠不得同時併用，圖片僅供參考，產品以實物為準，炸雞部位恕不開放挑選，皆由門市人員搭配，3塊上校雞塊不提供糖醋醬，若需求糖醋醬需依店內加價購買。 如遇不可抗力或原物料短缺等因素，以致門市無法提供相關商品，肯德基有權以等值商品替代，詳情請以店內公告為主，肯德基保有修改活動辦法及優惠內容的權利。 優惠區域: 全台 優惠日期: 2018-07-22 ~ 2018-09-30', 'img':'https://s3.goodlife.tw/system/att/000/017/845/image/1532314581.jpg', 'startDate':'2018-07-22', 'endDate':'2018-09-30'}}

        self.BKOldData = {'漢堡王暑期宵夜限定優惠 買8塊上校雞塊送香酥脆薯':{'desc' :'即日起至2018/8/27，晚間9:00後至餐廳打烊間， 暑期宵夜限定優惠\n買8塊上校雞塊送香酥脆薯(中)\n限餐廳內用、外帶使用，不適用電話外送、網路訂餐與自助點餐機\n晚間9:00後至餐廳打烊間，至肯德基購買才有優惠喔\n期間限定優惠，只到2018/8/27\n區域: 全台 優惠日期: 2018-08-03 ~ 2018-08-27', 'img':'https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png', 'startDate':'2018-08-03', 'endDate':'2018-08-27'},
                        '漢堡王 芒果莎莎咔啦雞腿堡7/31新上市 嘗鮮優惠券 ':{'desc':'肯德基芒果莎莎咔啦雞腿堡7/31新上市\n經典咔啦雞腿排，淋上融合鮮甜芒果泥的清爽莎莎醬，\n再夾入墨西哥脆餅，爽脆萵苣， 蓋上鬆軟芝麻麵包！\n多層次的豐富口感，\n示嘗鮮優惠券， 品嘗夏季限定的美味\n嚐鮮期間：2018/7/31~ 2018/8/27。\n優惠區域: 全台 優惠日期: 2018-07-31 ~ 2018-08-27', 'img':'https://s3.goodlife.tw/system/att/000/017/851/image/1532991351.jpg', 'startDate':'2018-07-31', 'endDate':'2018-08-27'},
                        '漢堡王 GoodLife 爸氣雙饗餐 限時優惠券':{'desc':'GoodLife粉絲團 爸氣雙饗餐 18261 1個咔啦脆雞堡+2塊咔啦脆雞+1份勁爆雞米花(大)+1份點心盒(上校雞塊+香酥脆薯)+2顆原味蛋撻+2杯百事可樂(小(原價386元))=NT$249 2018/7/22~2018/9/30\n注意事項: 1.本券可至全國肯德基餐廳使用(台北車站及宜蘭家樂福餐廳不適用)，結帳時出示優惠券(或手機圖檔)， 使用紙券使用後需回收。。 2.限正餐時段(10:30AM起供應)使用，使用期限：2018/7/22~2018/9/30(中秋連假9/22~9/24不適用)，優惠代碼18261。 3.本券不適用外送及網路訂餐，優惠不得同時併用，圖片僅供參考，產品以實物為準，炸雞部位恕不開放挑選，皆由門市人員搭配，3塊上校雞塊不提供糖醋醬，若需求糖醋醬需依店內加價購買。 如遇不可抗力或原物料短缺等因素，以致門市無法提供相關商品，肯德基有權以等值商品替代，詳情請以店內公告為主，肯德基保有修改活動辦法及優惠內容的權利。 優惠區域: 全台 優惠日期: 2018-07-22 ~ 2018-09-30', 'img':'https://s3.goodlife.tw/system/att/000/017/845/image/1532314581.jpg', 'startDate':'2018-07-22', 'endDate':'2018-09-30'}}

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

    

    def notify(self,subscribers):
        bot = self.bot
        for ID in subscribers["KFC"]:
            if len(self.KFCnewKeys) != 0:
                for key in self.KFCnewKeys:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,self.KFCCoupons))
                    bot.sendPhoto(ID,self.KFCCoupons[key]["img"])

            if len(self.KFClastDayCoupons) != 0:
                for key in self.KFClastDayCoupons:
                    bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,self.KFCCoupons))
                    bot.sendPhoto(ID,self.KFCCoupons[key]["img"])
        for ID in subscribers["BK"]:
            if len(self.BKnewKeys) != 0:
                for key in self.BKnewKeys:
                    bot.sendMessage(ID,self.tickets.printCoupon(key,self.BKCoupons))
                    bot.sendPhoto(ID,self.BKCoupons[key]["img"])
            if len(self.BKlastDayCoupons) != 0:
                for key in self.BKlastDayCoupons:
                    bot.sendMessage(ID,self.tickets.printLastDayCoupon(key,self.BKCoupons))
                    bot.sendPhoto(ID,self.BKCoupons[key]["img"])

    def execute(self,subscribers):
        self.update()
        self.notify(subscribers) 
        self.KFCOldData = self.KFCCoupons
        self.BKOldData = self.BKCoupons

    def setup(self):
        self.KFCCoupons = KFCSpider().get_coupons()
        self.BKCoupons = BKSpider().get_coupons()    
        print("[CouponModule] setup")
        schedule.every().day.at("10:14").do(self.execute,self.subscribers)
        #schedule.every().day.at("10:15").do(self.execute,self.subscribers)
        
    
        


    def loop(self):
        bot = self.bot
        schedule.run_pending()
        print("[CouponModule] loop")