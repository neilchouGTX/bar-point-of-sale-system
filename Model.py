import json
import os
class UsersModel():
    def __init__(self):
        folder_path = os.getcwd()  
        db_path=os.path.join(folder_path, "DBFilesJson")
        db_path=os.path.join(db_path, "dutchman_table_users.json")
        # Open and read the JSON file
        with open(db_path, 'r') as file:
            self.data = json.load(file)

    def getDataByUsername(self, username):
        for thedata in self.data:
            if thedata["username"]==username:
                return thedata
    
    def checkLogin(self, username, password):
        for thedata in self.data:
            if thedata["username"]==username and thedata["password"]==password:
                return thedata

class BeerStaticData():
    """save all the data of the beer"""
    def __init__(self, nr=None, namn=None, varugrupp=None, producent=None, ursprunglandnamn=None, alkoholhalt=None, prisinklmoms=None, forpackning=None):
        self.nr = nr  # number ID I think
        self.namn = namn  #  name
        self.varugrupp = varugrupp  # catalogue（EX: Beer or wine or wiskey）
        self.producent = producent  # producer
        self.ursprunglandnamn = ursprunglandnamn  # Origin
        self.alkoholhalt = alkoholhalt  # alc.
        self.prisinklmoms = prisinklmoms  # prices
        self.forpackning = forpackning  # packaging

        if self.nr:
            self.image = f"images/{self.nr}.png"  
        else:
            self.image = "images/default.png" 


class BeerModel():
    def __init__(self):
        folder_path = os.getcwd()  
        db_path = os.path.join(folder_path, "DBFilesJson", "dutchman_table_sbl_beer.json")

        # 讀取 JSON 檔案
        with open(db_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        
        self.varugrupps = []
        self.staticData = []
        self.jsonToObject()

    def jsonToObject(self):
        for theData in self.data:
            theStaticData = BeerStaticData()

            for key, value in theData.items():
                if hasattr(theStaticData, key):
                    setattr(theStaticData, key, value)

            self.staticData.append(theStaticData)
            if theStaticData.varugrupp not in self.varugrupps:
                self.varugrupps.append(theStaticData.varugrupp)

    def getDataByCategory(self, varugrupp):
        return [theData for theData in self.staticData if theData.varugrupp == varugrupp]

beerModel=BeerModel()

# category='Cognac'
# theData=beerModel.getDataByCategory(category)
# print(theData.__len__())



        