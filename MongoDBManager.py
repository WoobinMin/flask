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

        #총 데이터 숫자를 세주는 듯
        self.UserDatas_documents_count = self.db['UserDatas'].count_documents({})
        self.UserList_documents_count = self.db['UserList'].count_documents({})
        self.Tumblbug_documents_count = self.db['Tumblbug'].count_documents({})

    
    def GetUserDatasCount(self):
        return self.UserDatas_documents_count
    
    def GetUserListCount(self):
        return self.UserList_documents_count
    
    def GetTumblbugCount(self):
        return self.Tumblbug_documents_count