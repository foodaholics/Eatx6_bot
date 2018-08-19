import requests
from bs4 import BeautifulSoup
from pprint import pprint

class twentyOneCenturySpider:
    def get_coupons(self):
        newData = {}

        # link_1 = 'https://goodlife.tw/%E9%80%9F%E9%A3%9F%E5%BA%97/%E8%82%AF%E5%BE%B7%E5%9F%BA'# KFC 可用
        # link_1 = 'https://goodlife.tw/%E9%80%9F%E9%A3%9F%E5%BA%97/%E6%BC%A2%E5%A0%A1%E7%8E%8B' # BK





        #------------第二部分 顯示有哪些餐卷------------------------------------------------
        #產生網址
        for i in range(1,11):
            link_1 = 'https://goodlife.tw/%E9%80%9F%E9%A3%9F%E5%BA%97/21%E4%B8%96%E7%B4%80%E9%A2%A8%E5%91%B3%E9%A4%A8/page/'
            link_1 = link_1 + str(i)

        #擷取網址內容
            visitWeb2 = requests.get(link_1)
            soup = BeautifulSoup(visitWeb2.text, 'html.parser')
            brand_articles = soup.find(id='board') # 到date zone 位置
            tmp = brand_articles.findAll('ul')

            # post time
            for i in tmp[1:]:
                postTime = i.find('time')
                postTime = postTime.get_text()


        # 各優惠券 name / link
            for i in tmp[1:]:
                postTime = i.find('time') # 取postTime
                postTime = postTime.get_text()

                topic = i.find('li', {'class': 'topic'}) # 取 name and link
                name = topic.a.get_text().replace('\n', '').strip()
                link = topic.a['href']
                if '(已過期)' not in name and postTime.find('2018') != -1 : #取未過期的 and postYear 2018
                    # print('name:',name)
                    # print('link:',link)
                    # print("------  內容  ------")



        #-------------------第三部分 顯示折價卷內容------------------------------------
        #爬 折價券內容  desc / startDate / endDate / zone / img

                    link_2 = link
                    visitWeb3 = requests.get(link_2)
                    soup = BeautifulSoup(visitWeb3.text, 'html.parser')
                    coupon_articles = soup.find(id='content_html') #img desc
                    tmp = coupon_articles.findAll('p')

        ## 爬 折價券內容
                    descText = coupon_articles.get_text()
                    descText = descText.replace('\n','')
                    descText = descText.replace(' ', '')
                    # pprint(descText)




        ## 爬 優惠日期 / 優惠區域
                    findDateZone = soup.find(id="board") # get zone / startDate / endDate
                    DateZone = findDateZone.find('div', 'other_details')
                    wase = DateZone.find('br').get_text().strip().split('\n')
                    # pprint(wase)##########測試用
                    for i in range(len(wase)):
                        wase[i] = wase[i].strip()
                    # print('\n'.join(wase))
                    zone = wase[0]
                    date = wase[1]
                    # print(zone)################################################
                    # print(date)################################################
                    #
                    zone = zone[zone.find(' '):]
                    date = date[date.find(' '):]
                    # print('zone:', zone)
                    # print('date:', date)
                    if len(date) == 24:
                        date = date.split('~') # 分跟開始與結束時間
                        startDate = date[0].strip()
                        endDate = date[1].strip()
                    else:
                        date = date.strip()
                        startDate = date
                        endDate = date


                    # print('startDate:', startDate)##############################################
                    # print('endDate:', endDate)################################################


        # 爬 折價卷照片
                    img = coupon_articles.findAll('img')#.get('src') #get 圖片--okokokokokokokokokokokokokokokokokokokokokokokokokokokokokkoko
                    # print('img:')
                    imgList = []
                    for i in img :
                        img = i.get('src')
                        imgList.append(img)
                        # print(imgList) #get 圖片--okokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokokok
                    # print(descText)
                    # print(startDate)
                    # print(endDate)
                    newData[name] = {'desc':descText, 'img':imgList, 'startDate':startDate, 'endDate':endDate }
        # 清除無期限
        for i in newData:
            a = newData[i]['startDate']
            if a == '無期限':
                del newData[i]['startDate']

        return newData