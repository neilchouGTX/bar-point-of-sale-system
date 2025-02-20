from tkinter import *
import json
from tkinter import PhotoImage

class OrderView(Frame):
    def __init__(self,root,controller):
        super().__init__(root)
        self.controller=controller
        self.Cart=[]
        self.menuData=[]
        self.varugrupps=["Cognac", "Vitt vin","Okryddad sprit"]
        self.display()

    def display(self):
        self.menuGUI()
        self.shoppingCartGUI()
        self.varugruppsGUI()

        self.varugruppsFrame.grid(row=0,column=0)
        self.menuFrame.grid(row=1,column=0)
        self.shoppingCartFrame.grid(row=1,column=1)
    def varugruppsGUI(self):
        self.varugruppsFrame=Frame(self)

        for index,vargrupp in enumerate(self.varugrupps):
            theButton=Button(self.varugruppsFrame,text=vargrupp,command=lambda vg=vargrupp :self.getMenuData(vg))
            theButton.grid(row=1,column=index,padx=5)
        
        backButoon=Button(self.varugruppsFrame,text="back",command=self.backLoginPage)
        backButoon.grid(row=0,column=0)
        
    def menuGUI(self):
        self.menuFrame=Frame(self)

        self.title_lbl = Label(self.menuFrame, text ='Menu', 
                font = "50")  

        self.title_lbl.grid(row=0,column=0)
        
        self.menu_srb = Scrollbar(self.menuFrame) 
        
        self.menu_srb.grid(row=1,column=1,sticky="wns") 
        
        self.menu_list = Listbox(self.menuFrame,width=25,height=10,  
                        yscrollcommand = self.menu_srb.set ) 
        
        self.getMenuData(self.varugrupps[0])
        
        for theData in self.menuData: 
            self.menu_list.insert(END, theData.namn) 
        
        self.menu_list.grid(row=1,column=0)
        
        self.menu_srb.config( command = self.menu_list.yview ) 

        add_btn=Button(self.menuFrame,text="Add wine",command=self.addItem)
        add_btn.grid(row=2,column=0)  

    def shoppingCartGUI(self):
        self.shoppingCartFrame=Frame(self)
        self.title_lbl = Label(self.shoppingCartFrame, text ='Shopping Cart', 
                font = "50")  

        self.title_lbl.grid(row=0,column=2)
        
        self.cart_srb = Scrollbar(self.shoppingCartFrame) 
        
        self.cart_srb.grid(row=1,column=3,sticky="ns",) 
        
        self.Cart_list = Listbox(self.shoppingCartFrame,width=25,height=10,  
                        yscrollcommand = self.cart_srb.set ) 

            
        
        self.Cart_list.grid(row=1,column=2,)
        
        self.cart_srb.config( command = self.Cart_list.yview ) 
        send_btn=Button(self.shoppingCartFrame,text="Send Order",command=self.sendOrder)
        send_btn.grid(row=2,column=2)
        
        
    ### Button Function ###
    def addItem(self):
        indices = self.menu_list.curselection()
        theBeer=self.menuData[indices[0]]
        exist=False
        for theItem in self.Cart:
            if theItem.name==theBeer.namn:
                theItem.add()
                exist=True

        if not exist:
            self.Cart.append(Item(theBeer.namn,id=theBeer.nr))
        
        print(json.dumps([theItem.__dict__ for theItem in self.Cart]))
        
        self.Cart_list.delete(0,END)

        for theItem in self.Cart:
            self.Cart_list.insert(END,str(f"{theItem.name} x {theItem.count}"))
    
    def sendOrder(self):
        indices = self.Cart_list.curselection()
        theWine = self.wines[indices[0]]
        print(theWine)
    
    def getMenuData(self,varugrupp):
        self.menuData=self.controller.getMenuData(varugrupp)
        self.menu_list.delete(0,END)

        for theData in self.menuData:
            self.menu_list.insert(END, theData.namn)
    
    def backLoginPage(self):
        self.controller.view.show_frame("LoginView")
class Item ():
    def __init__(self,name,id=1,count=1):
        self.id=id
        self.name=name
        self.count=count
    def add(self):
        self.count+=1
    def __str__(self):
        return f"name:{self.name}, count:{self.count}"

    
    
    



    


"""
import os

folder_path = os.getcwd()  # 當前目錄
images_path=os.path.join(folder_path, "images")
print(images_path)

image = PhotoImage(file=os.path.join(images_path,"shopping-cart.png"))
image=image.subsample(5,5)
send_label = Label(root, image=image)
send_label.grid(row=3,column=2)

root.mainloop() 
"""