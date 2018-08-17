import time
import datetime

class Ticket():
    def __init__(self):
        self.today = datetime.date.today().strftime("%Y-%m-%d")

    def getNewCoupon(self,oldData,newData): #用這個key去送出newDict裡面的新折價卷
        newKeys = []
        for data in newData.keys():
            if data not in oldData:
                newKeys.append(data)
        return newKeys

    def getLastDayCoupon(self,newData): #回傳是今日是最後一天的折價卷key
        lastDayCouponKeys = []
        for key in newData.keys():
            if newData[key]["endDate"] == self.today:
                lastDayCouponKeys.append(key)
        return lastDayCouponKeys
    
    def printCoupon(self,newKey,newData): # 只處理一則coupon
        data = newData[newKey]
        msg = newKey+"\n"+data["desc"]+"\n"+"開始時間："+data["startDate"]+"\n"+"結束時間："+data["endDate"]
        return msg

    def printLastDayCoupon(self,lastDayCouponKey,newData):
        data = newData[lastDayCouponKey]
        msg = lastDayCouponKey+" 要過期囉！"+"\n"+"結束時間："+data["endDate"]+"\n"
        msg += data["desc"]
        return msg