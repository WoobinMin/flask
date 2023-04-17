from pymongo import MongoClient
import matplotlib.pyplot as plt

class Converter:
    def __init__(self) -> None:
        self.mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
        self.pltTitle = ""
                
    def ConnectToDB(self) :
        # Connect To DB
        self.client = MongoClient(self.mongodb_URI)
        self.db = self.client['Hynpytol']

        #for문 사용시마다 초기화필요 (Cursor 자료형인듯)
        self.UserDatas_documents = self.db['UserDatas'].find({})

        #총 데이터 숫자를 세주는 듯
        self.UserDatas_documents_count = self.db['UserDatas'].count_documents({})
        self.UserList_documents_count = self.db['UserList'].count_documents({})
        plt.figure(figsize=(15,8))

    def AddPlaytimePlot(self):
        # Make PlayTimeDictionary
        playTimeDic = {}
        checkCount = {}

        self.UserDatas_documents = self.db['UserDatas'].find({})
        for i, document in enumerate(self.UserDatas_documents, 1):
            camPos = document['CamPosName']
            playTime = document['PlayTime']
            if camPos in playTimeDic :
                playTimeDic[camPos] = playTimeDic[camPos] + playTime
                checkCount[camPos] = checkCount[camPos] + 1     
            else :
                playTimeDic[camPos] = playTime       
                checkCount[camPos] = 1     

        for key in playTimeDic:
            playTimeDic[key] = playTimeDic[key] / checkCount[key]

        # Average PlayTimePlot
        y = playTimeDic.values()
   
        self.pltTitle += 'Checked Data(PlyaTime) : ' + str(self.UserDatas_documents_count) + '/'
        plt.plot(y , 'r' , label='Average PlayTime (s)')

    def AddHookCountPlot(self):
        hookCountDic = {}
        checkCount = {}

        self.UserDatas_documents = self.db['UserDatas'].find({})
        for i, document in enumerate(self.UserDatas_documents, 1):
            camPos = document['CamPosName']
            hookCount = document['HookCount']
            if camPos in hookCountDic :
                hookCountDic[camPos] = hookCountDic[camPos] + hookCount
                checkCount[camPos] = checkCount[camPos] + 1     
            else :
                hookCountDic[camPos] = hookCount       
                checkCount[camPos] = 1     

        for key in hookCountDic:
            hookCountDic[key] = hookCountDic[key] / checkCount[key]

        # Average PlayTimePlot
        y = hookCountDic.values()
   
        self.pltTitle += 'Checked Data(HookCount) : ' + str(self.UserDatas_documents_count) + '/'
        plt.plot(y , 'g' , label='Average HookCount')

    def AddUndoCountPlot(self):
        undoCountDic = {}
        checkCount = {}

        self.UserDatas_documents = self.db['UserDatas'].find({})
        for i, document in enumerate(self.UserDatas_documents, 1):
            camPos = document['CamPosName']
            undoCount = document['UndoCount']
            if camPos in undoCountDic :
                undoCountDic[camPos] = undoCountDic[camPos] + undoCount
                checkCount[camPos] = checkCount[camPos] + 1     
            else :
                undoCountDic[camPos] = undoCount       
                checkCount[camPos] = 1     

        for key in undoCountDic:
            undoCountDic[key] = undoCountDic[key] / checkCount[key]

        # Average PlayTimePlot
        y = undoCountDic.values()
   
        self.pltTitle += 'Checked Data(UndoCount) : ' + str(self.UserDatas_documents_count) + '/'
        plt.plot(y , 'b' , label='Average UndoCount')

    def AddRetryCountPlot(self):
        retryCountDic = {}
        checkCount = {}

        self.UserDatas_documents = self.db['UserDatas'].find({})
        for i, document in enumerate(self.UserDatas_documents, 1):
            camPos = document['CamPosName']
            retryCount = document['RetryCount']
            if camPos in retryCountDic :
                retryCountDic[camPos] = retryCountDic[camPos] + retryCount
                checkCount[camPos] = checkCount[camPos] + 1     
            else :
                retryCountDic[camPos] = retryCount       
                checkCount[camPos] = 1     

        for key in retryCountDic:
            retryCountDic[key] = retryCountDic[key] / checkCount[key]

        # Average PlayTimePlot
        y = retryCountDic.values()
   
        self.pltTitle += 'Checked Data(RetryCount) : ' + str(self.UserDatas_documents_count) + '/'
        plt.plot(y , 'c' , label='Average RetryCount')

    def AddPlayerCountPlot(self):
        playerCount = {}
        UserDatas_documents = self.db['UserDatas'].find({})
        for document in UserDatas_documents:
            camPos = document['CamPosName']
            uuid = document['UUID']
            if camPos not in playerCount :
                playerCount[camPos] = []
                playerCount[camPos] += [uuid]
            else :
                if uuid not in playerCount[camPos] :
                    playerCount[camPos] += [uuid]
            
        

        y = []
        for item in playerCount:
            y.append(len(playerCount[item]))

        self.pltTitle += 'Total Player : ' + str(self.UserList_documents_count) + '/'
        plt.plot(y , 'm' , label='PlayerCount')

    def SavePlot(self):
        
        camPoses = []
        UserDatas_documents = self.db['UserDatas'].find({})
        for document in UserDatas_documents:
            camPos = document['CamPosName']
            if camPos not in camPoses :
                camPoses.append(camPos)

        x = []
        for i in range(0,50):
            x.append(i)
        plt.xticks(x, camPoses)

        plt.title(self.pltTitle)
        plt.xlabel('Cam Pos Name')
        plt.legend()
        plt.savefig('static/img/output.jpg')




#ConvertToJPG()
