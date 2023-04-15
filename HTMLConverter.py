from pymongo import MongoClient
from numpy import np
import matplotlib.pyplot as plt


def ConvertToHTML() :
    # Connect To DB
    mongodb_URI = "mongodb://admin:1229@svc.sel3.cloudtype.app:30778/?authMechanism=DEFAULT"
    client = MongoClient(mongodb_URI)
    db = client['Hynpytol']
    type_documents = db['UserDatas'].find({})
    type_documents_count = db['UserDatas'].count_documents({})

    # Make PlayTimeDictionary
    playTimeDic = {}
    playCount = {}

    for i, document in enumerate(type_documents, 1):
            camPos = document['CamPosName']
            playTime = document['PlayTime']
            if camPos in playTimeDic :
                playTimeDic[camPos] = playTimeDic[camPos] + playTime
                playCount[camPos] = playCount[camPos] + 1     
            else :
                playTimeDic[camPos] = playTime       
                playCount[camPos] = 1     

    for key in playTimeDic:
        playTimeDic[key] = playTimeDic[key] / playCount[key]

    # Plot 생성
    x = np.arange(len(playTimeDic))
    y = playTimeDic.values()

    plt.xlabel('Cam Pos Name')
    plt.ylabel('Average Play Time')
    plt.plot(x,y)

    plt.savefig('static/img/output.jpg')

    return plt

    # HTML 생성 및 오픈
    # html_path = "C:/Users/1/Desktop/temp/HynpytolVisual/templates/VisualHTML.html"
    # html = mpld3.fig_to_html(f, figid='QADataVisual')

    # with open(html_path, "w") as file:
    #     file.write(html)
    #     file.close()


# fileMerge.MergeFile(collection)



# tempCode


# output_path = os.getcwd()+"/output/2ndQAbyDB.json"
# with open(output_path, "w") as file:
#     file.write('[')
#     # Start from one as type_documents_count also starts from 1.
#     for i, document in enumerate(type_documents, 1):
#         camPos = document['CamPosName']
#         del document['_id']
#         del document['DateTime']
#         del document['UUID']
#         pprint.pprint(document['PlayTime'])
#         file.write(json.dumps(document, default=str, indent=2))
#         if i != type_documents_count:
#             file.write(',')
#     file.write(']')
#     file.close()