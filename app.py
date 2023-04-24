from flask import Flask, render_template, request
import JPGConverter
import os
import CrawlingTumblbug
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

img = os.path.join('static', 'img')
 
@app.route('/', methods = ['GET' , 'POST'])
def main():
    cvt = JPGConverter.Converter()
    cvt.ConnectToDB()
    if(request.method == 'POST'):
        
        if request.form['Refresh'] == "Refresh":
            if request.form.get('PlayTime'):
                cvt.AddPlaytimePlot()

            if request.form.get('HookCount'):
                cvt.AddHookCountPlot()

            if request.form.get('UndoCount'):
                cvt.AddUndoCountPlot()

            if request.form.get('RetryCount'):
                cvt.AddRetryCountPlot()

            if request.form.get('PlayerCount'):
                cvt.AddPlayerCountPlot()

            cvt.SavePlot()
            file = os.path.join(img,'output.jpg')
        return render_template('VisualHTML.html', image=file)
        
    else :
        cvt.AddPlaytimePlot()
        cvt.AddHookCountPlot()
        cvt.AddUndoCountPlot()
        cvt.AddRetryCountPlot()
        cvt.AddPlayerCountPlot()

        cvt.SavePlot()
        file = os.path.join(img,'output.jpg')
        return render_template('VisualHTML.html', image=file)

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
