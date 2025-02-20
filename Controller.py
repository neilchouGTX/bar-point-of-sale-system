from views.Login_view import *
from Model import *
from views.Order_view import*
from Base_view import *
class Controller():
    def __init__(self):
        ## Model
        self.userModel=UsersModel()
        self.beerModel=BeerModel()
        
        ## View
        self.view=BaseView(self)

    def toggle_language_menu(self):
        if self.view.UpperViewlanguage_frame.winfo_ismapped():
            self.view.language_frame.place_forget()
        else:
            self.view.language_frame.place(x=1200, y=50)
            self.view.language_frame.lift()

    def toggle_drinks_menu(self):
        if self.view.drinks_menu_frame.winfo_ismapped():
            self.view.drinks_menu_frame.place_forget()
        else:
            self.view.drinks_menu_frame.place(x=100, y=90)
            self.view.drinks_menu_frame.lift()
            self.model.get_drinks_list()
    
    def displayView(self):
        self.view.display()
    
    def Login(self,username,password):
        userData=self.userModel.checkLogin(username,password)
        if userData!=None:
            print("Login success")
        else:
            print("Login fail")
    def getMenuData(self,varugrupp):
        theData=self.beerModel.getDataByCategory(varugrupp)
        return theData
    def refreshOrderView(self, category):
        # make orderViewNew refresh
        order_view = self.view.frames.get("OrderViewNew")
        if order_view:
            order_view.refresh(category)