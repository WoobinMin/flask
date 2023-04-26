from flask import Flask, render_template, request
import CrawlingTumblbug
import os
import ChartDataMaker
import MongoDBManager
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

img = os.path.join('static', 'img')
 
@app.route('/', methods = ['GET' , 'POST'])
def main():
    cralwer = CrawlingTumblbug.Crawler()
    chartMaker = ChartDataMaker.ChartDataMaker()
    mongoDBManager = MongoDBManager.MongoDBManager()

    chartMaker.MakeChartDataToCSV()

    priceNmemberCountList = cralwer.GetPriceNMemeberCount()
    
    price=priceNmemberCountList[0]
    memeberCount=priceNmemberCountList[1]
    dataCount=mongoDBManager.GetUserDatasCount()
    userCount=mongoDBManager.GetUserListCount()

    cralwer = CrawlingTumblbug.Crawler()
    cralwer.ConnectToDB()
    cralwer.CrawlingAndSaveTumblbug()

    return render_template('index.html', price=price, memberCount=memeberCount,dataCount=dataCount, userCount=userCount)

def ExcuteCrawler():
    cralwer = CrawlingTumblbug.Crawler()
    cralwer.ConnectToDB()
    cralwer.CrawlingAndSaveTumblbug()

scheduler = BackgroundScheduler()
scheduler.add_job(func=ExcuteCrawler, trigger="cron", minute=0)
scheduler.start()
 
atexit.register(lambda:scheduler.shutdown())

if __name__ == '__main__':
    app.run()
