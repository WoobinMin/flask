import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pytz
from datetime import datetime

class Crawler:
    def __init__(self) -> None:
        self.url = 'https://www.tumblbug.com/base0'
        self.mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
        self.ConnectToDB()
        
    def ConnectToDB(self) :
        # Connect To DB
        self.client = MongoClient(self.mongodb_URI)
        self.db = self.client['Hynpytol']
        self.document = self.db['Tumblbug']

    def CrawlingAndSaveTumblbug(self) :
        print("Crawling...")
        response = requests.get(self.url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            price = soup.select_one('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.hklIjO > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-11.ksxAKQ > div:nth-child(1) > div.ProjectIntroduction__StatusValue-sc-1o2ojgb-14.gMNqnP > span.ProjectIntroduction__Price-sc-1o2ojgb-15.jSZJkM')
            memberCount = soup.select_one('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.hklIjO > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-11.ksxAKQ > div:nth-child(3)')
            
            KST = pytz.timezone('Asia/Seoul')
            sys_date = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
            
            doc = {'DateTime': sys_date,'price':price.getText(),'MemberCount':memberCount.getText()}
            self.document.insert_one(doc)

            print("Crawling Success!")
        else : 
            print(response.status_code)
            print("Crawling Failed!")

    def GetPriceNMemeberCount(self):
        print("Crawling...")
        response = requests.get(self.url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            price = soup.select_one('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.hklIjO > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-11.ksxAKQ > div:nth-child(1) > div.ProjectIntroduction__StatusValue-sc-1o2ojgb-14.gMNqnP > span.ProjectIntroduction__Price-sc-1o2ojgb-15.jSZJkM')
            memberCount = soup.select_one('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.hklIjO > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-11.ksxAKQ > div:nth-child(3)')

            res = [price.getText(), memberCount.getText().split("후원자")[1]]

            print("Crawling Success!")
            return res
        else : 
            print(response.status_code)
            print("Crawling Failed!")
            return None
        
    def GetData(self, selector):
        print("Crawling...")
        response = requests.get(self.url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            data = soup.select_one(selector)

            return data.getText()
        else : 
            print(response.status_code)
            print("Crawling Failed!")
            return None
        

# crawler = Crawler()
# crawler.ConnectToDB()
# crawler.CrawlingAndSaveTumblbug()

