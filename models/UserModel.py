import json
import os

# class UsersModel():
#     def __init__(self):
#         folder_path = os.getcwd()  
#         db_path = os.path.join(folder_path, "DBFilesJson")
#         db_path = os.path.join(db_path, "dutchman_table_users.json")
#         # Open and read the JSON file
#         with open(db_path, 'r') as file:
#             self.data = json.load(file)

#     def getDataByUsername(self, username):
#         for thedata in self.data:
#             if thedata["username"] == username:
#                 return thedata
    
#     def checkLogin(self, username, password):
#         for thedata in self.data:
#             if thedata["username"] == username and thedata["password"] == password:
#                 return thedata
class UserModel:
    """
    用戶資料模型
    User Data Model
    """
    def __init__(self):
        # 使用者類型: 'VIP' 或 'Staff'
        # User type: 'VIP' or 'Staff'
        self.user_type = None

        # 是否已登入
        # Whether the user is logged in
        self.is_logged_in = False

        # 簡易存放 VIP 電話或員工ID
        # Simple storage for VIP phone or staff ID
        self.identifier = None

    def login(self, user_type, identifier):
        """
        登入 - 將使用者類型與識別資訊記錄到模型中
        Login - Store user type and identifier in the model
        """
        self.user_type = user_type
        self.identifier = identifier
        self.is_logged_in = True

    def logout(self):
        """
        登出 - 清除使用者相關資訊
        Logout - Clear user-related information
        """
        self.user_type = None
        self.identifier = None
        self.is_logged_in = False