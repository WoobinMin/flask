from flask import Flask, render_template, request
import DataParser_BIC2023
import os
import DataMakerByMongoDB
import MongoDBManager
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

img = os.path.join('static', 'img')
 
@app.route('/', methods = ['GET' , 'POST'])
def main():
    dataMaker = DataMakerByMongoDB.DataMakerByMongoDB('Hynpytol' , 'UserDatas_BIC2023', 'UserList_BIC2023')
    dataMaker.MakeJsonFile("2023-08-26")
    dataMaker.MakeJsonFile("2023-08-27")
    #mongoDBManager = MongoDBManager.MongoDBManager()

    bicParser = DataParser_BIC2023.DataParser_BIC2023(dataMaker.GetAssignedUserDatas(), dataMaker.GetAssignedUserLists())

    day1Data = bicParser.GetDayData("2023-08-26")
    day2Data = bicParser.GetDayData("2023-08-27")


    return render_template('index.html', 
                           day1TotalPlayTime=day1Data.dayTotalPlayTime, 
                           day1TotalDataCount=day1Data.dayTotalDataCount, 
                           day1TotalPlayerCount=day1Data.dayTotalPlayerCount, 
                           day2TotalPlayTime=day2Data.dayTotalPlayTime, 
                           day2TotalDataCount=day2Data.dayTotalDataCount, 
                           day2TotalPlayerCount=day2Data.dayTotalPlayerCount, 
                           )

if __name__ == '__main__':
    app.run()
