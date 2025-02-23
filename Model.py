import json
import os

class UsersModel():
    def __init__(self):
        folder_path = os.getcwd()  
        db_path = os.path.join(folder_path, "DBFilesJson")
        db_path = os.path.join(db_path, "dutchman_table_users.json")
        # Open and read the JSON file
        with open(db_path, 'r') as file:
            self.data = json.load(file)

    def getDataByUsername(self, username):
        for thedata in self.data:
            if thedata["username"] == username:
                return thedata
    
    def checkLogin(self, username, password):
        for thedata in self.data:
            if thedata["username"] == username and thedata["password"] == password:
                return thedata

class BeerStaticData():
    """用來儲存單個酒品的資訊"""
    def __init__(self, nr=None, namn=None, varugrupp=None, producent=None, ursprunglandnamn=None, alkoholhalt=None, prisinklmoms=None, forpackning=None):
        self.nr = nr  # 商品編號
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

    def getDataByCategory(self, varugrupp):
        return [theData for theData in self.staticData if theData.varugrupp == varugrupp]

beerModel = BeerModel()

# New Stock data models
class StockData:
    """用來儲存單個飲品的庫存數據"""
    def __init__(self, beverage_id, amount=0):
        self.beverage_id = beverage_id
        self.amount = amount

class StockModel:
    """管理所有飲品的庫存數據，基於 JSON 文件"""
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), "DBFilesJSON", "dutchman_table_sbl_beer_stock.json")
        self.data = []
        self.stock = {}
        self.sorted_data = []  # Cache for sorted data
        self.load_stock()

    def load_stock(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.stock = {item["nr"]: item["total_stock"] for item in self.data}
        self.sorted_data = sorted(self.data, key=lambda x: x["nr"])

    def save_stock(self):
        # Update the total_stock in self.data from self.stock
        for item in self.data:
            key = item["nr"]
            if key in self.stock:
                item["total_stock"] = self.stock[key]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        # Refresh the sorted cache after saving
        self.sorted_data = sorted(self.data, key=lambda x: x["nr"])

    def update_stock(self, beverage_id, amount):
        self.stock[beverage_id] = amount
        self.save_stock()

    def get_stock(self, beverage_id):
        return self.stock.get(beverage_id, 0)

    def add_beverage(self, beverage):
        # beverage is a dict with keys matching the JSON schema.
        self.data.append(beverage)
        self.stock[beverage["nr"]] = beverage.get("total_stock", 0)
        self.save_stock()

    def remove_beverage(self, beverage_name):
        removed = False
        for item in self.data:
            if item["namn"] == beverage_name:
                key = item["nr"]
                self.data.remove(item)
                if key in self.stock:
                    del self.stock[key]
                removed = True
                break
        self.save_stock()
        return removed

    def view_total_stock(self):
        total = sum(self.stock.values())
        details = "\n".join([f"{item['namn']} (nr: {item['nr']}): {item['total_stock']}" for item in self.data])
        return total, details
    
    def view_total_stock_page(self, page=1, page_size=20):
        import math
        total = sum(self.stock.values())
        total_items = len(self.sorted_data)
        total_pages = math.ceil(total_items / page_size)
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        start = (page - 1) * page_size
        end = start + page_size
        page_items = self.sorted_data[start:end]
        details = "\n".join([f"{item['namn']} (nr: {item['nr']}): {item['total_stock']}" for item in page_items])
        return total, details, page, total_pages


stockModel = StockModel()
