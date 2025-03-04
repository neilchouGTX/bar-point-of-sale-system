import os
import json

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
        """Load initial stock data into memory."""
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
        # Update stock for a specific beverage
        self.stock[beverage_id] = amount
        self.save_stock()

    def get_stock(self, beverage_id):
        #Get stock amount for a specific beverage.
        return self.stock.get(beverage_id, 0)

    def add_beverage(self, beverage):
        # beverage is a dict with keys matching the JSON schema.
        self.data.append(beverage)
        self.stock[beverage["nr"]] = beverage.get("total_stock", 0)
        self.save_stock()

    def remove_beverage(self, beverage_name):
        # Remove a beverage from the stock by name.
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
        #View total stock 
        total = sum(self.stock.values())
        details = "\n".join([f"{item['namn']} (nr: {item['nr']}): {item['total_stock']}" for item in self.data])
        return total, details
    

    def view_total_stock_page(self, page=1, page_size=20, filter_text=""):
        # View stock data for a specific page
        import math
        with open(self.file_path, 'r', encoding='utf-8') as f:
            f.seek(1)  # Skip the opening '['
            items = []
            while True:
                line = f.readline().strip()
                if line == ']':
                    break
                if line.endswith(','):
                    line = line[:-1]
                try:
                    item = json.loads(line)
                    # Apply filter if provided
                    if not filter_text or filter_text.lower() in item["nr"].lower() or filter_text.lower() in item["namn"].lower():
                        items.append(item)
                except json.JSONDecodeError:
                    continue  # Skip invalid lines

        total_items = len(items)
        total_pages = math.ceil(total_items / page_size)
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        start = (page - 1) * page_size
        end = start + page_size
        page_items = items[start:end]
        details = "\n".join([f"{item['namn']} (nr: {item['nr']}): {item['total_stock']}" for item in page_items])
        total = sum(item['total_stock'] for item in items)
        return total, details, page, total_pages

stockModel = StockModel()