import os
import json

class OrderItem:
    def __init__(self, item_id, amount, price):
        self.id = item_id
        self.amount = amount
        self.price = price
class Order:
    def __init__(self, table_number, orderItems,totalPrice):
        self.tableNumber = table_number
        self.totalPrice = totalPrice
        self.orderItems = orderItems


class OrderModel:
    def __init__(self):
        self.data=[]
        folder_path = os.getcwd()  
        self.db_path=os.path.join(folder_path, "DBFilesJson", "dutchman_order.json")

        self.loadData()
        self.staticData=[]
        self.jsonToObject()
        self.saveData()
    def loadData(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            with open(self.db_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
    
    def saveData(self):
        # """
        # orders = [
        #     Order(5, [OrderItem(101, 2, 50.0), OrderItem(102, 1, 30.0)],1000),
        #     Order(3, [OrderItem(201, 1, 25.0), OrderItem(202, 4, 15.0)],1000),
        #     Order(7, [OrderItem(301, 3, 40.0)],10000)]
        # """
        # # 轉換所有訂單為字典列表
        # orders_data = [order.__dict__ for order in self.staticData]

        # # 進一步轉換 Item 為字典
        # for order in orders_data:
        #     order["orderItems"] = [item.__dict__ for item in order["orderItems"]]

        # # 存入 JSON 檔案
        # with open(self.db_path, "w", encoding="utf-8") as file:
        #     json.dump(orders_data, file, ensure_ascii=False, indent=4)
        orders_data = []
        for order in self.staticData:
            # 將 Order 物件轉換成 dict
            order_dict = {
                "tableNumber": order.tableNumber,
                "totalPrice": order.totalPrice,
                "orderItems": []
            }
            # 將每個 OrderItem 物件轉換成 dict
            for item in order.orderItems:
                item_dict = {
                    "id": int(item.id),
                    "amount": item.amount,
                    "price": item.price
                }
                order_dict["orderItems"].append(item_dict)
            orders_data.append(order_dict)
        
        # 寫入 JSON 檔案，格式如範例中所示
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(orders_data, file, ensure_ascii=False, indent=4)
        
    def jsonToObject(self):
        self.staticData = [
            Order(
                table_number=order["tableNumber"],
                orderItems=[OrderItem(item["id"], item["amount"], item["price"]) for item in order["orderItems"]],
                totalPrice=order["totalPrice"]
            )
            for order in self.data
        ]
        
    def add_order(self, table_number, cart_data):
        order_items = []
        total_price = 0.0

        # 將每個購物車項目轉換成 OrderItem
        for item in cart_data:
            price = float(item.prisinklmoms)
            quantity = int(item.quantity)
            order_item = OrderItem(item.nr, quantity, price)
            order_items.append(order_item)
            total_price += price * quantity

        # 建立新的 Order 物件
        new_order = Order(table_number, order_items, total_price)

        # 將訂單加入 OrderModel 的資料中，並寫入 JSON
        self.staticData.append(new_order)
        self.saveData()

        print(f"Order for table {table_number} with total price {total_price:.2f} has been saved.")