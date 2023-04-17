from pymongo import MongoClient
import matplotlib.pyplot as plt
import pprint

def ConvertToJPG() :
    # Connect To DB / Make Figure 
    mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
    client = MongoClient(mongodb_URI)
    db = client['Hynpytol']

    #for문 사용시마다 초기화필요 (Cursor 자료형인듯)
    UserDatas_documents = db['UserDatas'].find({})

    #총 데이터 숫자를 세주는 듯
    UserDatas_documents_count = db['UserDatas'].count_documents({})
    UserList_documents_count = db['UserList'].count_documents({})
    plt.figure(figsize=(20,20))

#region Mak PlayTime Plot

    # Make PlayTimeDictionary
    playTimeDic = {}
    playCount = {}

    for i, document in enumerate(UserDatas_documents, 1):
            camPos = document['CamPosName']
            playTime = document['PlayTime']
            uuid = document['UUID']
            if camPos in playTimeDic :
                playTimeDic[camPos] = playTimeDic[camPos] + playTime
                playCount[camPos] = playCount[camPos] + 1     
            else :
                playTimeDic[camPos] = playTime       
                playCount[camPos] = 1     

            

    for key in playTimeDic:
        playTimeDic[key] = playTimeDic[key] / playCount[key]

    # Average PlayTimePlot
    plt.subplot(2,1,1)
    x = []
    xTicks = list(playTimeDic.keys())
    for i in range(0,50):
        x.append(i)
    y = playTimeDic.values()
    plt.xticks(x, xTicks)
   
    plt.xlabel('Cam Pos Name')
    plt.ylabel('Average Play Time')
    plt.title(label='Total Data : ' + str(UserDatas_documents_count))
    plt.plot(x,y)

#endregion


#region Make Player Count Plot
    # Player Count
    playerCount = {}
    UserDatas_documents = db['UserDatas'].find({})
    for document in UserDatas_documents:
        camPos = document['CamPosName']
        uuid = document['UUID']
        if camPos not in playerCount :
            playerCount[camPos] = []
            playerCount[camPos] += [uuid]
        else :
            if uuid not in playerCount[camPos] :
                playerCount[camPos] += [uuid]
        
    

    plt.subplot(2,1,2)
    plt.xticks(x, xTicks)
    plt.yticks(range(0, UserList_documents_count + 1))
    plt.xlabel('Cam Pos Name')
    plt.ylabel('Player Count')
    plt.ylim([0,UserList_documents_count])
    y = []
    for item in playerCount:
        y.append(len(playerCount[item]))

    plt.title(label='Total Player : ' + str(UserList_documents_count))
    plt.plot(x,y)

    
#endregion

    # Save as jpg
    plt.savefig('static/img/output.jpg')

    return plt

ConvertToJPG()
