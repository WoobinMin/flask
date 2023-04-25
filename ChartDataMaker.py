from pymongo import MongoClient
import csv

class ChartDataMaker:
    def __init__(self) -> None:
        self.mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
                
    def ConnectToDB(self) :
        # Connect To DB
        self.client = MongoClient(self.mongodb_URI)
        self.db = self.client['Hynpytol']

        #for문 사용시마다 초기화필요 (Cursor 자료형인듯)
        self.UserDatas_documents = self.db['UserDatas'].find({})

        #총 데이터 숫자를 세주는 듯
        self.UserDatas_documents_count = self.db['UserDatas'].count_documents({})
        self.UserList_documents_count = self.db['UserList'].count_documents({})

    
    def MakeChartData(self):
        # CSV String Member
        x = []

        #region PlayTimeDictionary
        playTimeDic = {}
        checkPlayTimeCount = {}
        
        hookCountDic = {}
        checkHookCount = {}

        undoCountDic = {}
        checkUndoCount = {}

        retryCountDic = {}
        checkRetryCount = {}

        self.UserDatas_documents = self.db['UserDatas'].find({})
        for i, document in enumerate(self.UserDatas_documents, 1):
            camPos = document['CamPosName']
            playTime = document['PlayTime']
            if camPos in playTimeDic :
                playTimeDic[camPos] = playTimeDic[camPos] + playTime
                checkPlayTimeCount[camPos] = checkPlayTimeCount[camPos] + 1     
            else :
                playTimeDic[camPos] = playTime       
                checkPlayTimeCount[camPos] = 1     


            hookCount = document['HookCount']
            if camPos in hookCountDic :
                hookCountDic[camPos] = hookCountDic[camPos] + hookCount
                checkHookCount[camPos] = checkHookCount[camPos] + 1     
            else :
                hookCountDic[camPos] = hookCount       
                checkHookCount[camPos] = 1  

            undoCount = document['UndoCount']
            if camPos in undoCountDic :
                undoCountDic[camPos] = undoCountDic[camPos] + undoCount
                checkUndoCount[camPos] = checkUndoCount[camPos] + 1     
            else :
                undoCountDic[camPos] = undoCount       
                checkUndoCount[camPos] = 1 
            
            retryCount = document['RetryCount']
            if camPos in retryCountDic :
                retryCountDic[camPos] = retryCountDic[camPos] + retryCount
                checkRetryCount[camPos] = checkRetryCount[camPos] + 1     
            else :
                retryCountDic[camPos] = retryCount       
                checkRetryCount[camPos] = 1  


        for key in playTimeDic:
            playTimeDic[key] = playTimeDic[key] / checkPlayTimeCount[key]

        for key in hookCountDic:
            hookCountDic[key] = hookCountDic[key] / checkHookCount[key]

        for key in undoCountDic:
            undoCountDic[key] = undoCountDic[key] / checkUndoCount[key]

        for key in retryCountDic:
            retryCountDic[key] = retryCountDic[key] / checkRetryCount[key]

        for key in playTimeDic:
            x.append([key, playTimeDic[key], hookCountDic[key] , undoCountDic[key] , retryCountDic[key]])
        #endregion
        

        with open('static/document/QAData.csv', 'w' , newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["CamPos","PlayTime", "HookCount" , "UndoCount" , "RetryCount"])
            writer.writerows(x)
