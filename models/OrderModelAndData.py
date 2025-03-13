import os
import json

class OrderItem:
    def __init__(self, item_id, amount, price, paid):
        self.id = item_id
        self.amount = amount
        self.price = price
        self.paid = paid
class Order:
    def __init__(self, table_number, orderItems,totalPrice, fullPaid):
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
                orderItems=[OrderItem(item["id"], item["amount"], item["price"], item["paid"]) for item in order["orderItems"]],
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

        existing_order = None
        self.refresh()
        for order in self.staticData:
            if order.tableNumber == table_number:
                existing_order = order
                break

        if existing_order:
            existing_order.totalPrice += new_order.totalPrice

            for new_item in new_order.orderItems:
                found = False
                for exist_item in existing_order.orderItems:
                    if str(exist_item.id) == str(new_item.id):
                        exist_item.amount += new_item.amount
                        new_item.paid = exist_item.paid
                        found = True
                        break
                if not found:
                    existing_order.orderItems.append(new_item)
        else:
            self.staticData.append(new_order)

        self.saveData()
        print(f"Order for table {table_number} with total price {total_price:.2f} has been saved.")

    def merge_orders_to_objects(self):
        with open(self.db_path, "r", encoding="utf-8") as file:
            orders = json.load(file)

        order_objects = []
        for order in orders:
            order_items = [
                OrderItem(item["id"], item["amount"], item["price"], item["paid"])
                for item in order["orderItems"]
            ]
            order_obj = Order(
                table_number=order["tableNumber"],
                orderItems=order_items,
                totalPrice=order["totalPrice"],
                fullPaid=order["fullPaid"]
            )
            order_objects.append(order_obj)
        
        return order_objects
    
    def orders_object_to_json(self, orders):
        orders_data = []
        for order in orders:
            order_dict = {
                "tableNumber": order.tableNumber,
                "totalPrice": order.totalPrice,
                "fullPaid": order.fullPaid,
                "orderItems": []
            }
            for item in order.orderItems:
                item_dict = {
                    "paid": item.paid,
                    "id": item.id,
                    "amount": item.amount,
                    "price": item.price
                }
                order_dict["orderItems"].append(item_dict)
            orders_data.append(order_dict)

        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(orders_data, file, ensure_ascii=False, indent=4)
        
    def archive_orders_to_json(self, orders):
        orders_data = []
        for order in orders:
            order_dict = {
                "tableNumber": order.tableNumber,
                "totalPrice": order.totalPrice,
                "fullPaid": order.fullPaid,
                "orderItems": []
            }
            for item in order.orderItems:
                item_dict = {
                    "id": int(item.id),
                    "amount": item.amount,
                    "price": item.price,
                    "paid": item.paid
                }
                order_dict["orderItems"].append(item_dict)
            orders_data.append(order_dict)
        return orders_data
    
    def refresh(self):
        self.loadData()
        self.jsonToObject()
        self.saveData()

    def archive_full_paid_order(self, table_number):
        """
        檢查指定桌號的訂單是否全數付清：
        - 如果該桌所有訂單的每個 OrderItem 的 paid >= amount，
            則將該訂單的 fullPaid 設為 True，
            並從目前訂單中刪除，再將其附加到 dutchman_legacy_order.json 中。
        """
        # 先過濾出要處理的訂單與其餘訂單
        self.refresh()
        full_paid_orders = []
        remaining_orders = []
        for order in self.staticData:
            if order.tableNumber == table_number:
                # 若每個 item 的 paid 都大於或等於 amount
                if all(item.paid >= item.amount for item in order.orderItems):
                    order.fullPaid = True
                    full_paid_orders.append(order)
                else:
                    remaining_orders.append(order)
            else:
                remaining_orders.append(order)
        
        # 更新目前的訂單資料
        if full_paid_orders:
            self.staticData = remaining_orders
            self.saveData()
            # 接著寫入 legacy JSON 檔案
            legacy_path = os.path.join(os.getcwd(), "DBFilesJson", "dutchman_legacy_order.json")
            if os.path.exists(legacy_path):
                with open(legacy_path, "r", encoding="utf-8") as file:
                    legacy_data = json.load(file)
            else:
                legacy_data = []
            # 將 full_paid_orders 轉換成 dict 格式
            full_paid_data = self.archive_orders_to_json(full_paid_orders)
            legacy_data.extend(full_paid_data)
            with open(legacy_path, "w", encoding="utf-8") as file:
                json.dump(legacy_data, file, ensure_ascii=False, indent=4)
