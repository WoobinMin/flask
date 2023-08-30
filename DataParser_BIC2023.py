import DataMakerByMongoDB

class DayData_BIC2023 :
    def __init__(self) -> None:
        self.dayTotalPlayTime = 0.0
        self.dayTotalDataCount = 0
        self.dayTotalPlayerCount = 0
        pass

class DataParser_BIC2023:
    def __init__(self, userStageDatas = [], userListDatas = []) -> None:
        self.userStageDatas = userStageDatas
        self.userListDatas = userListDatas

    def GetDayData(self, dateTime : str) -> DayData_BIC2023:
        dayData = DayData_BIC2023()
        dayData.dayTotalPlayTime = self.GetDayTotalPlayTime(dateTime)
        dayData.dayTotalDataCount = self.GetDayTotalDataCount(dateTime)
        dayData.dayTotalPlayerCount = self.GetDayTotalPlayerCount(dateTime)
        return dayData


    def GetDayTotalPlayTime(self, dateTime : str) -> float:
        result = 0.0
        for userListData  in self.userListDatas:
            date = userListData.startDate.split()[0]
            if dateTime in date:
                result += userListData.totalPlayTime

        return result
    
    def GetDayTotalPlayerCount(self, dateTime : str) -> float:
        result = 0
        for userListData  in self.userListDatas:
            date = userListData.startDate.split()[0]
            if dateTime in date:
                result += 1

        return result
    
    def GetDayTotalDataCount(self, dateTime : str) -> float:
        result = 0
        for userListData  in self.userListDatas:
            date = userListData.startDate.split()[0]
            if dateTime in date:
                result += userListData.visitedStages.__len__()

        return result
        

# crawler = Crawler()
# crawler.ConnectToDB()
# crawler.CrawlingAndSaveTumblbug()

