from tkinter import *
from tkinter import ttk
import json
from tkinter import PhotoImage
from Model import MenuItem
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
        self.setMenuView()
      
        self.varugruppsFrame.grid(row=0,column=0)
        self.menuFrame.grid(row=1,column=0)
        self.shoppingCartFrame.grid(row=1,column=1)
        self.setMenuViewFrame.grid(row=2,column=0)
        

    def varugruppsGUI(self):
        self.varugruppsFrame=Frame(self)

        for index,vargrupp in enumerate(self.varugrupps):
            theButton=Button(self.varugruppsFrame,text=vargrupp,command=lambda vg=vargrupp :self.getMenuData(vg))
            theButton.grid(row=1,column=index,padx=5)
        
        backButoon=Button(self.varugruppsFrame,text="back",command=self.backLoginPage,)
        backButoon.grid(row=0,column=0,)
        
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
        
    def setMenuView(self):
        self.setMenuViewFrame=Frame(self)

        self.title_lbl = Label(self.setMenuViewFrame, text ='Add Menu',) 
        self.title_lbl.grid(row=0,column=0)

        self.id_lbl=Label(self.setMenuViewFrame,text="id")
        self.id_lbl.grid(row=1,column=0)
        self.price_lbl=Label(self.setMenuViewFrame,text="price")
        self.price_lbl.grid(row=1,column=1)
        values=[]
        beerData=self.controller.beerModel.staticData
        for index,theData in enumerate(beerData):
            #print(theData.nr)
            values.append(f"{theData.nr} " + "," +theData.namn)
            if index>20:
                break

        self.combo_box = ttk.Combobox(self.setMenuViewFrame, values=values,width=10)
        self.combo_box.grid(row=2,column=0,padx=5)
        #self.price=StringVar()
        #self.price_ent=Entry(self.setMenuViewFrame,textvariable=self.price,width=10)
        #self.price_ent.grid(row=2,column=1,padx=5)

        self.addMenuBtn=Button(self.setMenuViewFrame,text="Add to the Menu",command=self.addItemtoMenu)
        self.addMenuBtn.grid(row=2,column=2,padx=5)

    
        self.id_lbl=Label(self.setMenuViewFrame,text="id")
        self.id_lbl.grid(row=3,column=0)
        self.name_lbl=Label(self.setMenuViewFrame,text="name")
        self.name_lbl.grid(row=3,column=1)
        #self.price_lbl=Label(self.setMenuViewFrame,text="price")
        #self.price_lbl.grid(row=3,column=2)

        self.refreshMenu()
        
    def refreshMenu(self):
        for widget in self.setMenuViewFrame.winfo_children():
            grid_info = widget.grid_info()  # 取得元件的 grid 位置
            if grid_info and grid_info["row"] >= 4 and grid_info["column"] >= 0:
                widget.destroy()  # 或 widget.grid_forget()
        for index,theItem in enumerate(self.controller.menuModel.staticData):
            self.id_lbl=Label(self.setMenuViewFrame,text=theItem.id)
            self.id_lbl.grid(row=4+index,column=0)
            self.name_lbl=Label(self.setMenuViewFrame,text=theItem.name)
            self.name_lbl.grid(row=4+index,column=1)
            #self.price_lbl=Label(self.setMenuViewFrame,text=theItem.price)
            #self.price_lbl.grid(row=4+index,column=2)
            self.remove_btn=Button(self.setMenuViewFrame,text="Remove",command=lambda i=index :self.removeItemFromMenu(i))
            self.remove_btn.grid(row=4+index,column=3)

    def addItemtoMenu(self):
        
        data=self.combo_box.get()
        data=data.split(",")
        
        id=data[0].strip()
        name=data[1].strip()
        #price=self.price.get()
        theItem=MenuItem(id,name)
        self.controller.addItemToMenu(theItem)
        self.refreshMenu()
    def removeItemFromMenu(self,index):
        self.controller.removeItemFromMenu(index)
        self.refreshMenu()
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