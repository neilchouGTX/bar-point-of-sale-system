import os
import json

class CartData:
    def __init__(self, nr, namn, prisinklmoms, quantity):
        self.nr = nr
        self.namn = namn
        self.prisinklmoms = prisinklmoms
        self.quantity = quantity

class CartModel:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), "DBFilesJSON", "dutchman_table_cart.json")
        self.cart_data = []
        self.load_data()

    def clear_cart(self):
        """清空購物車"""
        self.cart_data = []
        self.save_data()

    def load_data(self):
        """讀取本地 JSON，如果檔案不存在就維持空的 cart_data。"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.cart_data = [CartData(item["nr"], item["namn"], item["prisinklmoms"], item["quantity"]) for item in data]
        else:
            self.cart_data = []

    def save_data(self):
        """將 cart_data 寫回 JSON 檔。"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([vars(item) for item in self.cart_data], f, indent=4, ensure_ascii=False)

    def add_to_cart(self, drink_data):
        """將飲品加入購物車"""
        for item in self.cart_data:
            if item.nr == drink_data.nr:
                item.quantity += 1
                self.save_data()
                return
        
        new_item = CartData(drink_data.nr, drink_data.namn, drink_data.prisinklmoms, 1)
        self.cart_data.append(new_item)
        self.save_data()

    def remove_from_cart(self, drink_data):
        """從購物車移除飲品"""
        for item in self.cart_data:
            if item.nr == drink_data.nr:
                item.quantity -= 1
                if item.quantity <= 0:
                    self.cart_data.remove(item)
                self.save_data()
                return

    def get_quantity(self, drink_data):
        """取得購物車中某個飲品的數量"""
        for item in self.cart_data:
            if item.nr == drink_data.nr:
                return item.quantity
        return 0
    
    def get_cart_data(self):
        """取得購物車內所有的飲品數據"""
        return self.cart_data