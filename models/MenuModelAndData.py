import os
import json

class MenuItem:
    def __init__(self,id,name):
        self.id=id
        self.name=name
        #self.price=price
class MenuModel:
    def __init__(self):
        self.data=[]
        folder_path = os.getcwd()  
        self.db_path=os.path.join(folder_path, "DBFilesJson", "dutchman_menu.json")

        self.loadData()
        self.staticData=[]
        self.jsonToObject()
    def loadData(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            with open(self.db_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)

    def saveData(self,):
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(self.staticData, file, ensure_ascii=False, indent=4,default=self.custom_encoder)
    
    def custom_encoder(self,obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)
    
    def jsonToObject(self):
        for theData in self.data:
            theStaticData = MenuItem(1,2)
            for key, value in theData.items():
                if hasattr(theStaticData, key):
                    setattr(theStaticData, key, value)
            self.staticData.append(theStaticData)
    def getData(self):
        return self.staticData
    def addItem(self,menuData):
        self.staticData.append(menuData)
        self.saveData()
    def removeItem(self,index):
        self.staticData.pop(index)
        self.saveData()