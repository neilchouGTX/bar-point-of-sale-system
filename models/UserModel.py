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


class VIPModel(UserModel):
    """
    管理VIP使用者的資料，繼承自UserModel
    Manages VIP user data, inherits from UserModel.
    """
    def __init__(self, data_file="DBFilesJSON/dutchman_VIP_account.json"):
        self.user_type = None
        self.is_logged_in = False
        self.identifier = None
        self.data_file = data_file
        self.vip_users = []
        self.load_users()

    def load_users(self):
        """
        從JSON檔案載入VIP使用者資料到內存中
        Load VIP user data from JSON file into memory.
        """
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.vip_users = [
            {
                "user_id": user.get("user_id"),
                "credentials": user.get("credentials"),
                "password": user.get("password"),
                "phone": user.get("phone"),
                "username": user.get("username"),
                "balance": float(user.get("balance", 0))
            }
            for user in data
        ]

    def verify_login_by_phone(self, phone):
        """
        使用電話號碼進行登入驗證，成功則將使用者資料記錄於模型中
        Verify login using phone number.
        """
        for user in self.vip_users:
            if user["phone"] == phone:
                self.login('VIP', phone)
                return True
        return False

    def get_user_info_by_phone(self, phone):
        """
        根據電話號碼取得VIP用戶資訊，包括用戶名和餘額
        Get VIP user information by phone, including username and balance.
        """
        for user in self.vip_users:
            if user["phone"] == phone:
                return user
        return None