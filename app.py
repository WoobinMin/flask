from flask import Flask, render_template, request
import DataParser_BIC2023
import os
import DataMakerByMongoDB
import MongoDBManager
import atexit

app = Flask(__name__)

img = os.path.join('static', 'img')
 
@app.route('/', methods = ['GET' , 'POST'])
def main():
    dataMaker = DataMakerByMongoDB.DataMakerByMongoDB('Hynpytol' , 'UserDatas', 'UserList')
    dataMaker.MakeAllDatas()
    #mongoDBManager = MongoDBManager.MongoDBManager()

    bicParser = DataParser_BIC2023.DataParser_BIC2023(dataMaker.GetAssignedUserDatas(), dataMaker.GetAssignedUserLists())

    day1Data = bicParser.GetData()


    return render_template('index.html', 
                           day1TotalPlayTime=day1Data.dayTotalPlayTime, 
                           day1TotalDataCount=day1Data.dayTotalDataCount, 
                           day1TotalPlayerCount=day1Data.dayTotalPlayerCount, 
                           )

if __name__ == '__main__':
    app.run()
