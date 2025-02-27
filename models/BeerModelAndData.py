import json
import os

class BeerStaticData():
    """用來儲存單個酒品的資訊"""
    def __init__(self, nr=None, artikelid=None, namn=None, varugrupp=None, producent=None, ursprunglandnamn=None, alkoholhalt=None, prisinklmoms=None, forpackning=None):
        self.nr = nr  # 商品編號
        self.artikelid = artikelid #another id
        self.namn = namn  # 酒品名稱
        self.varugrupp = varugrupp  # 分類（如：啤酒、紅酒、白酒）
        self.producent = producent  # 生產商
        self.ursprunglandnamn = ursprunglandnamn  # 產地
        self.alkoholhalt = alkoholhalt  # 酒精濃度
        self.prisinklmoms = prisinklmoms  # 價格（含稅）
        self.forpackning = forpackning  # 包裝方式（瓶裝/罐裝）

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
    def getSetMenuData(self):
        return self.staticData
    def getDataByCategory(self, varugrupp):
        return [theData for theData in self.staticData if theData.varugrupp == varugrupp]
    def getDataById(self,id):
        
        for theData in self.staticData:
            if theData.nr==id:
                return theData
        
        return None
    def getDataByIds(self,ids):
        result = [theData for theData in self.staticData if theData.nr in ids]
        return result

beerModel = BeerModel()