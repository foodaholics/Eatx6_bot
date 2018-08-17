class KFCSpider:
    def get_coupons(self):
        newData = {"肯德基暑期優惠":{"desc":"暑期優惠kfc","img":["https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png"],"startDate":"2018-08-13","endDate":"2018-09-10"}, # 新爬到的資料
            "肯德基暑期優惠飲料":{"desc":"暑期優惠","img":["https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png"],"startDate":"2018-08-17","endDate":"2018-09-10"},
            "肯德基寒假優惠":{"desc":"寒假優惠kfc","img":["https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png"],"startDate":"2018-08-14","endDate":"2018-08-14"},
            "肯德基寒假優惠飲料":{"desc":"寒假優惠","img":["https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png"],"startDate":"2018-08-13","endDate":"2018-09-10"},
            "肯德基優惠":{"desc":"寒假優惠","img":["https://s3.goodlife.tw/system/att/000/017/870/image/1533258791.png"],"startDate":"2018-08-14","endDate":"2018-09-10"}}
        return newData