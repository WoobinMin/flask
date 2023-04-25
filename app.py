from flask import Flask, render_template, request
import CrawlingTumblbug
import os
import ChartDataMaker
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

img = os.path.join('static', 'img')
 
@app.route('/', methods = ['GET' , 'POST'])
def main():
    cralwer = CrawlingTumblbug.Crawler()
    cralwer.ConnectToDB()
    priceNmemberCount = cralwer.GetPriceNMemeberCount()
    price=priceNmemberCount.split('/')[0]
    memeberCount=priceNmemberCount.split('/')[1]

    chartMaker = ChartDataMaker.ChartDataMaker()
    chartMaker.ConnectToDB()
    chartMaker.MakeChartData()

    return render_template('index.html', price=price, memberCount=memeberCount)

def ExcuteCrawler():
    cralwer = CrawlingTumblbug.Crawler()
    cralwer.ConnectToDB()
    cralwer.CrawlingAndSaveTumblbug()

scheduler = BackgroundScheduler(timezone='Asia/Seoul')
scheduler.add_job(func=ExcuteCrawler, trigger="cron", minute=0)
scheduler.start()
 
atexit.register(lambda:scheduler.shutdown())

if __name__ == '__main__':
    app.run()
