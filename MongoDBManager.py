from pymongo import MongoClient
import csv

class MongoDBManager:
    def __init__(self) -> None:
        self.mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
        self.ConnectToDB()
                
    def ConnectToDB(self) :
        # Connect To DB
        self.client = MongoClient(self.mongodb_URI)
        self.db = self.client['Hynpytol']

        self.UserDatas_documents = self.db['UserDatas'].find({})
        self.UserList_documents = self.db['UserList'].find({})

        #총 데이터 숫자를 세주는 듯
        self.UserDatas_documents_count = self.db['UserDatas'].count_documents({})
        self.UserList_documents_count = self.db['UserList'].count_documents({})
        self.Tumblbug_documents_count = self.db['Tumblbug'].count_documents({})

    def GetAllUserUUIDs(self):
        res = []
        self.UserList_documents.rewind()

        for i, document in enumerate(self.UserList_documents, 1):
            uuid = document['UUID']
            if uuid not in res :
                res.append(uuid)

        return res
    
    def GetAllUserStartDates(self):
        res = []
        self.UserList_documents.rewind()

        for i, document in enumerate(self.UserList_documents, 1):
            dateTime = document['DateTime']
            if dateTime not in res :
                res.append(dateTime)

        return res

    def GetAllLastPlayDates(self):
        res = []
        self.UserDatas_documents.rewind()
        userUUIDs = self.GetAllUserUUIDs()
        for uuid in userUUIDs:
            myQuery = {"UUID" : str(uuid)}
            all_documents = self.db['UserDatas'].find(myQuery)

            dateTimes = []
            for document in all_documents:
                dateTime = document['DateTime']
                dateTimes.append(dateTime)

            if len(dateTimes) == 0:
                res.append("null")
            else :
                res.append(dateTimes[-1])

        return res
    
    def GetAllLastStages(self):
        res = []
        self.UserDatas_documents.rewind()
        userUUIDs = self.GetAllUserUUIDs()
        for uuid in userUUIDs:
            myQuery = {"UUID" : str(uuid)}
            all_documents = self.db['UserDatas'].find(myQuery)

            stages = []
            for document in all_documents:
                stage = document['CamPosName']
                stages.append(stage)

            if len(stages) == 0:
                res.append("null")
            else :
                res.append(stages[-1])

        return res
    
    def GetAllTotalPlayTimes(self):
        res = []
        self.UserDatas_documents.rewind()
        userUUIDs = self.GetAllUserUUIDs()

        for uuid in userUUIDs:
            myQuery = {"UUID" : str(uuid)}
            all_documents = self.db['UserDatas'].find(myQuery)

            totalPlayTime = 0
            for document in all_documents:
                playTime = document['PlayTime']
                totalPlayTime = totalPlayTime + playTime

            res.append(totalPlayTime)

        return res

    def GetUserDatasCount(self):
        return self.UserDatas_documents_count
    
    def GetUserListCount(self):
        return self.UserList_documents_count
    
    def GetTumblbugCount(self):
        return self.Tumblbug_documents_count
    
