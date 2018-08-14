import requests
from bs4 import BeautifulSoup

class WeatherCrawler:
    def __init__(self, latitude= '25.043543', longitude= '121.534397'):
        self.latitude = latitude
        self.longitude = longitude
        url = "https://weather.com/zh-TW/weather/today/l/" + latitude + ',' + longitude
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('div', {'class': 'today_nowcard-section today_nowcard-condition'}).get_text()
        data = data.replace('°','°C')
        data = data.strip()
        rain = soup.find('span',{'class': 'today-wx-descrip'}).get_text()
        rain = data[data.find('降'):-1]
        a = ['C','體','高','紫']
        self.info = ""
        for i,j in zip(a,a[1:]):
            if i == 'C':
                start = data.find(i)+1
                temperature = '現在溫度 '+ data[:start]
                end = data.find(j)
                string = data[start:end]
                self.info += temperature  + rain + '\n' + string + '\n'
            else:
                if j == '紫':
                    start = data.find(i)
                    end = data.find(j)
                    high_low = data[start:end]
                    start = data.find(j)
                    sun = data[start:]
                    self.info += high_low + '\n' + sun
                else:
                    start = data.find(i)
                    end = data.find(j)
                    self.info += data[start:end] + '\n'
        print(self.info)
    def getInfo(self):
        return self.info