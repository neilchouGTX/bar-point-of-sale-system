import os
import json

class OrderItem:
    def __init__(self, item_id, amount, price, paid=0):
        self.id = item_id
        self.amount = amount
        self.price = price
        self.paid = paid
class Order:
    def __init__(self, table_number, orderItems,totalPrice, fullPaid=False):
        self.tableNumber = table_number
        self.totalPrice = totalPrice
        self.orderItems = orderItems
        self.fullPaid = fullPaid


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
                "fullPaid": order.fullPaid,
                "orderItems": [],
                
            }
            # 將每個 OrderItem 物件轉換成 dict
            for item in order.orderItems:
                item_dict = {
                    "paid": item.paid,
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
                orderItems=[OrderItem(item["id"], item["amount"], item["price"], paid=0) for item in order["orderItems"]],
                totalPrice=order["totalPrice"],
                fullPaid=False
            )
            for order in self.data
        ]
        
    def add_order(self, table_number, cart_data):
        # order_items = []
        # total_price = 0.0

        # # 將每個購物車項目轉換成 OrderItem
        # for item in cart_data:
        #     price = float(item.prisinklmoms)
        #     quantity = int(item.quantity)
        #     order_item = OrderItem(item.nr, quantity, price, paid=0)
        #     order_items.append(order_item)
        #     total_price += price * quantity

        # # 建立新的 Order 物件
        # new_order = Order(table_number, order_items, total_price, fullPaid=False)

        # # 將訂單加入 OrderModel 的資料中，並寫入 JSON
        # self.staticData.append(new_order)
        # self.saveData()

        # print(f"Order for table {table_number} with total price {total_price:.2f} has been saved.")
        order_items = []
        total_price = 0.0

        # 將購物車內的項目轉換成 OrderItem 並計算總價
        for item in cart_data:
            price = float(item.prisinklmoms)
            quantity = int(item.quantity)
            order_item = OrderItem(item.nr, quantity, price, paid=0)
            order_items.append(order_item)
            total_price += price * quantity

        new_order = Order(table_number, order_items, total_price, fullPaid=False)

        # 檢查是否已有該桌號的訂單
        existing_order = None
        for order in self.staticData:
            if order.tableNumber == table_number:
                existing_order = order
                break

        if existing_order:
            # 合併總價
            existing_order.totalPrice += new_order.totalPrice

            # 合併訂單項目：若已存在相同商品則累加數量，否則新增
            for new_item in new_order.orderItems:
                found = False
                for exist_item in existing_order.orderItems:
                    if exist_item.id == new_item.id:
                        exist_item.amount += new_item.amount
                        found = True
                        break
                if not found:
                    existing_order.orderItems.append(new_item)
        else:
            # 若無現存訂單，直接加入新的訂單
            self.staticData.append(new_order)

        self.saveData()
        print(f"Order for table {table_number} with total price {total_price:.2f} has been saved.")

    def merge_orders_to_objects(self):
        with open(self.db_path, "r", encoding="utf-8") as file:
            orders = json.load(file)
        
        merged_orders = {}

        for order in orders:
            table_number = order["tableNumber"]

            if table_number not in merged_orders:
                merged_orders[table_number] = {
                    "totalPrice": 0,
                    "orderItems": {}
                }

            merged_orders[table_number]["totalPrice"] += order["totalPrice"]

            for item in order["orderItems"]:
                item_id = item["id"]
                if item_id in merged_orders[table_number]["orderItems"]:
                    # existing item, add amount
                    merged_orders[table_number]["orderItems"][item_id].amount += item["amount"]
                else:
                    # new item, create OrderItem object
                    merged_orders[table_number]["orderItems"][item_id] = OrderItem(item["id"], item["amount"], item["price"])

        merged_orders_list = [
            Order(
                table_number=table,
                orderItems=list(details["orderItems"].values()),
                totalPrice=details["totalPrice"]
            )
            for table, details in merged_orders.items()
        ]
        
        return merged_orders_list