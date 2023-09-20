from pymongo import MongoClient
import json
import csv

class UserListData:
    def __init__(self) -> None:
        self.UUID = ""
        self.startDate = ""
        self.lastDate = ""
        self.visitedStages = []
        self.lastStage = UserStageData()
        self.totalPlayTime = 0

class UserStageData:
    def __init__(self) -> None:
        self.buildVersion = ""
        self.dateTime = ""
        self.UUID = ""
        self.camPosName = ""
        self.playTime = 0
        self.hookCount = 0
        self.undoCount = 0
        self.retryCount = 0

class StageAvgData:
    def __init__(self) -> None:
        self.playTimes = []
        self.hookCounts = []
        self.undoCounts = []
        self.retryCounts = []
        

class DataMakerByMongoDB:
    def __init__(self, clientName , userDatasDBName , userListsDBName) -> None:
        self.mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
        self.clientName = clientName
        self.userDatasDBName = userDatasDBName
        self.userListsDBName = userListsDBName
        
        self.userStageDatas = []
        self.userListDatas =[]

        self.ConnectToDB()

        #for문 사용시마다 초기화필요 (Cursor 자료형인듯)
        self.AssignUserDatas()
        self.AssignUserLists()
                
    def ConnectToDB(self) :
        # Connect To DB
        self.client = MongoClient(self.mongodb_URI)
        self.db = self.client[self.clientName]

    def RemoveMany(self):
        self.db.UserDatas.delete_many({ "DateTime": { "$regex": "2023-08" } })

    def UpdateMany(self):
        update_query = {"$set" : {"BuildVersion" : "Hynpytol 0.4.0"}}
        self.db.UserDatas.update_many({}, update_query)


    def AssignUserDatas(self) :
        userDatas_documents = self.db[self.userDatasDBName].find({})

        for i, document in enumerate(userDatas_documents, 1):
            userStageData = UserStageData()
            
            try : 
                userStageData.buildVersion = document['BuildVersion']
                userStageData.dateTime = document['DateTime']
                userStageData.UUID = document['UUID']
                userStageData.camPosName = document['CamPosName']
                userStageData.playTime = document['PlayTime']
                userStageData.hookCount = document['HookCount']
                userStageData.undoCount = document['UndoCount']
                userStageData.retryCount = document['RetryCount']
            except :
                continue

            self.userStageDatas.append(userStageData)

    def AssignUserLists(self):
        userList_documents = self.db[self.userListsDBName].find({})

        for i, document in enumerate(userList_documents, 1):
            userListData = UserListData()
            userListData.UUID = document['UUID']
            userListData.startDate = document['DateTime']

            filter = {"UUID" : userListData.UUID}
            userDatas_documents_byUUID = self.db[self.userDatasDBName].find(filter)

            for j, document in enumerate(userDatas_documents_byUUID, 1):
                userStageData = UserStageData()
                try : 
                    userStageData.buildVersion = document['BuildVersion']
                    userStageData.dateTime = document['DateTime']
                    userStageData.UUID = document['UUID']
                    userStageData.camPosName = document['CamPosName']
                    userStageData.playTime = document['PlayTime']
                    userStageData.hookCount = document['HookCount']
                    userStageData.undoCount = document['UndoCount']
                    userStageData.retryCount = document['RetryCount']

                    userListData.visitedStages.append(userStageData)
                    userListData.lastStage = userStageData
                    userListData.lastDate = userStageData.dateTime
                    userListData.totalPlayTime += userStageData.playTime
                except :
                    continue

            if(userListData.lastStage.camPosName == "") :
                continue
            else :
                self.userListDatas.append(userListData)

    def GetAssignedUserDatas(self) -> []:
        return self.userStageDatas
    
    def GetAssignedUserLists(self) -> []:
        return self.userListDatas
    
    def MakeAllDatas(self):
        #Data Json을
        #CamPos
        #PlayTime
        #HookCount
        #UndoCount
        #..
        #등 이런식으로 짜줘야함

        camPosDict = {}
        camPosDataCount = {}
        for data in self.userListDatas:
            for visitedStage in data.visitedStages:
                if visitedStage.camPosName in camPosDict:
                    #데이터값 더해주기
                    camPosDataCount[visitedStage.camPosName] += 1
                    camPosDict[visitedStage.camPosName].playTime += visitedStage.playTime
                    camPosDict[visitedStage.camPosName].hookCount += visitedStage.hookCount
                    camPosDict[visitedStage.camPosName].undoCount += visitedStage.undoCount
                    camPosDict[visitedStage.camPosName].retryCount += visitedStage.retryCount
                else:
                    camPosDataCount[visitedStage.camPosName] = 1
                    camPosDict[visitedStage.camPosName] = UserStageData()
                    camPosDict[visitedStage.camPosName].playTime = visitedStage.playTime
                    camPosDict[visitedStage.camPosName].hookCount = visitedStage.hookCount
                    camPosDict[visitedStage.camPosName].undoCount = visitedStage.undoCount
                    camPosDict[visitedStage.camPosName].retryCount = visitedStage.retryCount

        for key in camPosDict:
            camPosDict[key].playTime = round(camPosDict[key].playTime / camPosDataCount[key], 1)
            camPosDict[key].hookCount =  round(camPosDict[key].hookCount / camPosDataCount[key], 1)
            camPosDict[key].undoCount =  round(camPosDict[key].undoCount / camPosDataCount[key], 1)
            camPosDict[key].retryCount =  round(camPosDict[key].retryCount / camPosDataCount[key], 1)

        userStageDatas_Dic = [{"CamPosName" : key,
                               "PlayTime" : camPosDict[key].playTime,
                               "HookCount" : camPosDict[key].hookCount,
                               "UndoCount" : camPosDict[key].undoCount,
                               "RetryCount" : camPosDict[key].retryCount} for key in camPosDict]
        
        json_data = json.dumps(userStageDatas_Dic, indent=4)

        with open(f"./static/document/UserStageDatas.json", "w") as json_file:
            json_file.write(json_data)
    
    def MakeJsonFile(self, date : str):
        #Data Json을
        #CamPos
        #PlayTime
        #HookCount
        #UndoCount
        #..
        #등 이런식으로 짜줘야함

        camPosDict = {}
        camPosDataCount = {}
        for data in self.userListDatas:
            if data.startDate.split()[0] not in date :
                continue

            for visitedStage in data.visitedStages:
                if visitedStage.camPosName in camPosDict:
                    #데이터값 더해주기
                    camPosDataCount[visitedStage.camPosName] += 1
                    camPosDict[visitedStage.camPosName].playTime += visitedStage.playTime
                    camPosDict[visitedStage.camPosName].hookCount += visitedStage.hookCount
                    camPosDict[visitedStage.camPosName].undoCount += visitedStage.undoCount
                    camPosDict[visitedStage.camPosName].retryCount += visitedStage.retryCount
                else:
                    camPosDataCount[visitedStage.camPosName] = 1
                    camPosDict[visitedStage.camPosName] = UserStageData()
                    camPosDict[visitedStage.camPosName].playTime = visitedStage.playTime
                    camPosDict[visitedStage.camPosName].hookCount = visitedStage.hookCount
                    camPosDict[visitedStage.camPosName].undoCount = visitedStage.undoCount
                    camPosDict[visitedStage.camPosName].retryCount = visitedStage.retryCount

        for key in camPosDict:
            camPosDict[key].playTime = round(camPosDict[key].playTime / camPosDataCount[key], 1)
            camPosDict[key].hookCount =  round(camPosDict[key].hookCount / camPosDataCount[key], 1)
            camPosDict[key].undoCount =  round(camPosDict[key].undoCount / camPosDataCount[key], 1)
            camPosDict[key].retryCount =  round(camPosDict[key].retryCount / camPosDataCount[key], 1)

        userStageDatas_Dic = [{"CamPosName" : key,
                               "PlayTime" : camPosDict[key].playTime,
                               "HookCount" : camPosDict[key].hookCount,
                               "UndoCount" : camPosDict[key].undoCount,
                               "RetryCount" : camPosDict[key].retryCount} for key in camPosDict]
        
        json_data = json.dumps(userStageDatas_Dic, indent=4)

        with open(f"./static/document/UserStageDatas_{date}.json", "w") as json_file:
            json_file.write(json_data)


maker = DataMakerByMongoDB("Hynpytol" , "UserDatas" , "UserList")
maker.UpdateMany()