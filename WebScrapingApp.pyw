from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import sqlite3
import urllib
from urllib.request import urlopen

conn = sqlite3.connect("Scrab.db")
c = conn.cursor()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("Scrab.db")
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS trendyol(id integer primary key, product_name varchar(250), price text, ratings text)'''
            )
        self.c.execute(          
            '''CREATE TABLE IF NOT EXISTS getir(id integer primary key, product_name varchar(250), price text, ratings text)'''
            )
        self.conn.commit()

class Main(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db


        subcategory_url = StringVar()
    def init_main(self):
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='TRENDYOL')
        self.tabControl.add(self.tab2, text='GETIR')
        self.tabControl.add(self.tab3, text='GETIR BÜYÜK')

        self.subTabControlTrendyol = ttk.Notebook(self.tab1)
        self.subTabControlGetir = ttk.Notebook(self.tab2)
        self.subTabControlGetirBuyuk = ttk.Notebook(self.tab3)

        self.label_frame = LabelFrame(self.tab1, text='Goşmak we täzelemek: ')
        self.label_frame.pack(side='top', fill =X, padx=5, pady=5)
        self.pageIndexTrendyol = ttk.Combobox(self.label_frame,width = 27, textvariable = StringVar(), state = 'readonly')
        self.pageIndexTrendyol.bind('<<ComboboxSelected>>', self.onTrendyolCategorySelect)    
        self.pageIndexTrendyol.pack(side='left', padx=5, pady=5)
        self.pageIndexTrendyolEntry = Entry(self.label_frame)
        self.pageIndexTrendyolEntry.pack(side='left', padx=5, pady=5)
        self.getFromTrendyol = Button(self.label_frame, text='Trendyoldan goş', bd=1, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=self.importfromTrendyol)
        self.getFromTrendyol.pack(side='left', padx=5, pady=5)

        self.lblFrameGetir = LabelFrame(self.tab2, text='Goşmak we täzelemek: ')
        self.lblFrameGetir.pack(side='top', fill =X, padx=5, pady=5)
        self.pageIndexGetir = ttk.Combobox(self.lblFrameGetir,width = 27, textvariable = StringVar(), state = 'readonly')
        self.pageIndexGetir.bind('<<ComboboxSelected>>', self.onGetirCategorySelect)
        self.pageIndexGetir.pack(side='left', padx=5, pady=5)
        #self.pageIndexGetirEntry = ttk.Entry(self.lblFrameGetir)
        #self.pageIndexGetirEntry.pack(side='left', padx=5, pady=5)
        self.insertFromGetirButton = Button(self.lblFrameGetir, text="Getir-den goş", bd=1, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=self.importfromGetir)
        self.insertFromGetirButton.pack(side='left', padx=5, pady=5)

        self.lblFrameGetirBuyuk = LabelFrame(self.tab3, text='Goşmak we täzelemek: ')
        self.lblFrameGetirBuyuk.pack(side='top', fill =X, padx=5, pady=5)
        self.pageIndexGetirBuyuk = ttk.Combobox(self.lblFrameGetirBuyuk,width = 27, textvariable = StringVar(), state = 'readonly')
        self.pageIndexGetirBuyuk.bind('<<ComboboxSelected>>', self.onGetirBuyukCategorySelect)
        self.pageIndexGetirBuyuk.pack(side='left', padx=5, pady=5)
        #self.pageIndexGetirBuyukEntry = Entry(self.lblFrameGetirBuyuk)
        #self.pageIndexGetirBuyukEntry.pack(side='left', padx=5, pady=5)
        self.insertFromGetirBuyukButton = Button(self.lblFrameGetirBuyuk, text="Getir Büyük-den goş", bd=1, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2', command=self.importfromGetirBuyuk)
        self.insertFromGetirBuyukButton.pack(side='left', padx=5, pady=5)

    def clickbtn(self):
        text = 'Hello ' + str(self.num)
        self.tree.insert('', 'end', text=text)
        self.num += 1

    def delete(self,evt):
        pass
        
    def select_all(self):
        self.tree.select_range(0, END)
        self.tree.focus()
        selected = self.tree.selection()
       # print (self.tree.item(0)['text'])

    def popup(self, event):
        self.iid = self.tree.identify_row(event.y)
        if self.iid:
            # mouse pointer over item
            self.tree.selection_set(self.iid)
            self.aMenu.post(event.x_root, event.y_root)            
        else:
            pass

        self.subcategory_url = StringVar()
        page_index = IntVar()
        self.subcategory_id = IntVar()

    def onselect(self,evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        
    def onTrendyolCategorySelect(self,evt):
        w = evt.widget
        index = int(w.current())
        print(w.get())
        value = w.get()
        print('You selected item %d: "%s"' % (index, value))


    def onGetirCategorySelect(self,evt):
        w = evt.widget
        index = int(w.current())
        value = w.get()
        print('Saýlanan kategoriýa id: %d, ady: "%s"' % (index, value))

    def onGetirBuyukCategorySelect(self,evt):
        w = evt.widget
        index = int(w.current())
        value = w.get()
        print('Saýlanan kategoriýa id: %d, ady: "%s"' % (index, value))

    def on_tab_change(self,event):
        tab = event.widget.tab('current')['text']
        
        if tab == 'TRENDYOL':
            print(tab)
            self.subTabControlTrendyol.destroy()
            self.subTabControlTrendyol  = ttk.Notebook(self.tab1)
            self.subTabControlTrendyol.pack(expand=1,fill="both")
            db.c.execute("Select id, category_name from category_trendyol")
            self.categories = db.c.fetchall()
            for category in self.categories:
                self.cat_id = category[0]
                self.tab_name = category[1]
                self.tab_name  = ttk.Frame(self.subTabControlTrendyol)
                self.subTabControlTrendyol.add(self.tab_name, text = category[1])
                self.tree = ttk.Treeview(self.tab_name, column=("c1", "c2", "c3"), show='headings')
                self.tree.column("#1", anchor=CENTER)
                self.tree.heading("#1", text="ID")
                self.tree.column("#2", anchor=CENTER)
                self.tree.heading("#2", text="PRODUCT NAME")
                self.tree.column("#3", anchor=CENTER)
                self.tree.heading("#3", text="PRICE")
##                self.tree.column("#4", anchor=CENTER)
##                self.tree.heading("#4", text="SELL")
                self.tree.pack(expand=1, fill='both')
                self.aMenu = Menu(self.tab_name, tearoff=0)
                self.aMenu.add_command(label='Delete', command=self.delete)
                self.aMenu.add_command(label='Select All', command=self.select_all)
                self.num = 0
                self.tree.bind("<Button-3>", self.popup)
                self.db.c.execute("SELECT * from trendyol where category_id=?", (self.cat_id,))
                rows = self.db.c.fetchall()
                for row in rows:
                    self.tree.insert("", END, values=row)
                self.db.conn.commit()
##            canvas3.unbind_all()
##            canvas2.bind_all('<MouseWheel>', lambda event: canvas2.yview_scroll(int(-1 * (event.delta / 120)),"units"))
        elif tab == 'GETIR':
            print(tab)
            self.subTabControlGetir.destroy()
            self.subTabControlGetir  = ttk.Notebook(self.tab2)
            self.subTabControlGetir.pack(expand=1,fill="both")

            self.scrollBar = Scrollbar(self.subTabControlGetir, orient=HORIZONTAL)
            self.scrollBar.pack(side=BOTTOM, fill=X)
            
            db.c.execute("Select id, category_name from category_getir")
            self.categories = db.c.fetchall()
            for category in self.categories:
                self.cat_id = category[0]
                self.tab_name = category[1]
                self.tab_name  = ttk.Frame(self.subTabControlGetir)
                self.subTabControlGetir.add(self.tab_name, text = category[1])
                self.treeGetir = ttk.Treeview(self.tab_name, column=("c1", "c2", "c3"), show='headings')
                self.treeGetir.column("#1", anchor=CENTER)
                self.treeGetir.heading("#1", text="ID")
                self.treeGetir.column("#2", anchor=CENTER)
                self.treeGetir.heading("#2", text="PRODUCT NAME")
                self.treeGetir.column("#3", anchor=CENTER)
                self.treeGetir.heading("#3", text="PRICE")
                self.treeGetir.pack(expand=1, fill='both')
                self.aMenu = Menu(self.tab_name, tearoff=0)
                self.aMenu.add_command(label='Delete', command=self.delete)
                self.aMenu.add_command(label='Select All', command=self.select_all)
                self.num = 0
                self.treeGetir.bind("<Button-3>", self.popup)
                self.db.c.execute("SELECT * from getir where category_id=?", (self.cat_id,))
                rows = self.db.c.fetchall()
                for row in rows:
                    self.treeGetir.insert("", END, values=row)
                self.db.conn.commit()
        elif tab == 'GETIR BÜYÜK':
            print(tab)

            self.subTabControlGetirBuyuk.destroy()
            self.subTabControlGetirBuyuk  = ttk.Notebook(self.tab3)
            self.subTabControlGetirBuyuk.pack(expand=1,fill="both")

            db.c.execute("Select id, category_name from category_getirbuyuk")
            self.categories = db.c.fetchall()
            for category in self.categories:
                self.cat_id = category[0]
                self.tab_name = category[1]
                self.tab_name  = ttk.Frame(self.subTabControlGetirBuyuk)
                self.subTabControlGetirBuyuk.add(self.tab_name, text = category[1])
                self.GetirBuyuk = ttk.Treeview(self.tab_name, column=("c1", "c2", "c3"), show='headings')
                self.GetirBuyuk.column("#1", anchor=CENTER)
                self.GetirBuyuk.heading("#1", text="ID")
                self.GetirBuyuk.column("#2", anchor=CENTER)
                self.GetirBuyuk.heading("#2", text="PRODUCT NAME")
                self.GetirBuyuk.column("#3", anchor=CENTER)
                self.GetirBuyuk.heading("#3", text="PRICE")
                self.GetirBuyuk.pack(expand=1, fill='both')
                self.aMenu = Menu(self.tab_name, tearoff=0)
                self.aMenu.add_command(label='Delete', command=self.delete(self.GetirBuyuk))
                self.aMenu.add_command(label='Select All', command=self.select_all)
                self.num = 0
                self.GetirBuyuk.bind("<Button-3>", self.popup)
                self.db.c.execute("SELECT * from getirbuyuk where category_id=?", (self.cat_id,))
                rows = self.db.c.fetchall()
                for row in rows:
                    self.GetirBuyuk.insert("", END, values=row)                    
                self.db.conn.commit()
            

##                canvas2.unbind_all()
##            canvas3.bind_all('<MouseWheel>', lambda event: canvas3.yview_scroll(int(-1 * (event.delta / 120)), "units"))


    def on_Trendyol_tab_change(self,event):
        tab = event.widget.tab('current')['text']
        print(tab)

    def on_Getir_tab_change(self,event):
        tab = event.widget.tab('current')['text']
        print(tab)


    def on_GetirBuyuk_tab_change(self,event):
        tab = event.widget.tab('current')['text']
        print(tab)
##        self.db.c.execute('''SELECT * from getirbuyuk''')
##        rows = self.db.c.fetchall()
##        for row in rows:
##            print(row)
##            self.tree.insert("", END, values=row)
##        self.db.conn.commit()

    def importfromTrendyol(self):
        value = self.pageIndexTrendyol.get()
        self.db.c.execute("Select id, category_url from category_trendyol where category_name=?", (value,))
        categories = self.db.c.fetchall()
        for category in categories:                      
           self.subcategory_url = category[1]
           self.subcategory_id = category[0]

        self.page_index = int(self.pageIndexTrendyolEntry.get())
        print("page:" + str(self.page_index))      
        print("url:" + self.subcategory_url)
        print("id:" + str(self.subcategory_id))
        base_url = "https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/"+self.subcategory_url+"?pi="+str(self.page_index)+"&culture=tr-TR&userGenderId=1&pId=oILWmJijJM&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B"
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}

        try:
            request = urllib.request.Request(url=base_url,headers=headers)

            data_json = json.loads(urlopen(request).read())

            results = data_json.get('result')
            products = results.get('products')
            
            for product in products:
                pid = product.get('id')
                pname=product.get('name')
                price = product.get('price')
                sellingPrice = price.get('sellingPrice')
                try:
                    db.c.execute('''insert into trendyol(id,product_name, price, category_id) values(?,?,?,?)''', (pid,pname,sellingPrice, self.subcategory_id ))
                    db.conn.commit()
                except Exception as e:
                    try:
                        db.c.execute('''update trendyol set price=? where id=?''', (sellingPrice,pid))
                        db.conn.commit()
                    except Exception as es:
                        print(e)
            messagebox.showinfo("Maglumatlar goşuldy", "Maglumatlar baza üstünlikli goşuldy ýa-da täzelendi!")
        except Exception as he:
            print(he)
            messagebox.showerror("Ýalňyşlyk ýüze çykdy", "Internet birikmäňizi barlaň ýa-da gaýtadan synanşyň!")

        #self.getOldData()


    def importfromGetir(self):
        value = self.pageIndexGetir.get()
        self.db.c.execute("Select id, category_url from category_getir where category_name=?", (value,))
        categories = self.db.c.fetchall()
        for category in categories:                      
           self.subcategory_url = category[1]
           self.subcategory_id = category[0]

        print("url:" + self.subcategory_url)
        print("id:" + str(self.subcategory_id))

        base_url = "https://getirx-client-api-gateway.getirapi.com/category/products?countryCode=TR&categorySlug="+ self.subcategory_url
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
        print(base_url)
        try:
            request = urllib.request.Request(url=base_url,headers=headers)

            data_json = json.loads(urlopen(request).read())

            data = data_json.get('data')
            category = data.get('category')
            subcategories = category.get('subCategories')
            for subcategory in subcategories:
                products = subcategory.get('products')
                for product in products:
                    
                    pid = product.get('id')
                    price = product.get('price')
                    pname=product.get('name')
                    print(product.get('id'), product.get('name'), product.get('price'))
                    try:
                        db.c.execute('''insert into getir(id,product_name, price, category_id) values(?,?,?,?)''', (pid,pname,price, self.subcategory_id))
                        db.conn.commit()
                        
                    except Exception as e:
                        try:
                            db.c.execute('''update getir set price=? where id=?''', (price,pid))
                            db.conn.commit()
                        except Exception as es:
                            print(e)
        except Exception as he:
            print(he)
            messagebox.showerror("Ýalňyşlyk ýüze çykdy", "Internet birikmäňizi barlaň ýa-da gaýtadan synanşyň!")

    def importfromGetirBuyuk(self):
        value = self.pageIndexGetirBuyuk.get()
        self.db.c.execute("Select id, category_url from category_getirbuyuk where category_name=?", (value,))
        categories = self.db.c.fetchall()
        for category in categories:                      
           self.subcategory_url = category[1]
           self.subcategory_id = category[0]
     
        print("url:" + self.subcategory_url)
        print("id:" + str(self.subcategory_id))

        base_url = "https://market-client-api-gateway.getirapi.com/category/products?countryCode=TR&categorySlug="+ self.subcategory_url
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
        print(base_url)
        
        try:
            request = urllib.request.Request(url=base_url,headers=headers)

            data_json = json.loads(urlopen(request).read())

            data = data_json.get('data')
            category = data.get('category')
            subcategories = category.get('subCategories')
            for subcategory in subcategories:
                products = subcategory.get('products')
                for product in products:
                    
                    pid = product.get('id')
                    price = product.get('price')
                    pname=product.get('name')
                    print(product.get('id'), product.get('name'), product.get('price'))
                    try:
                        db.c.execute('''insert into getirbuyuk(id,product_name, price, category_id) values(?,?,?,?)''', (pid,pname,price, self.subcategory_id))
                        db.conn.commit()
                    except Exception as e:
                        try:
                            db.c.execute('''update getirbuyuk set price=? where id=?''', (price,pid))
                            db.conn.commit()
                        except Exception as es:
                            print(e)
        except Exception as he:
            print(he)
            messagebox.showerror("Ýalňyşlyk ýüze çykdy", "Internet birikmäňizi barlaň ýa-da gaýtadan synanşyň!")
            
    def getCategoryListTrendyol(self):
        self.db.c.execute('''SELECT category_name from category_trendyol''')
        row = self.db.c.fetchall()

        for item in row:
            self.pageIndexTrendyol['values']=tuple(list(self.pageIndexTrendyol['values'])) + item
        self.db.conn.commit()

    def getCategoryListGetir(self):
        self.db.c.execute('''SELECT category_name from category_getir''')
        row = self.db.c.fetchall()

        for item in row:
            self.pageIndexGetir['values']=tuple(list(self.pageIndexGetir['values'])) + item
        self.db.conn.commit()

    def getCategoryListGetirBuyuk(self):
        self.db.c.execute('''SELECT category_name from category_getirbuyuk''')
        row = self.db.c.fetchall()

        for item in row:
            self.pageIndexGetirBuyuk['values']=tuple(list(self.pageIndexGetirBuyuk['values'])) + item
        self.db.conn.commit()


if __name__ == "__main__":
    root = Tk()
    db= DB()
    app = Main(root)
    app.pack()
    app.tabControl.pack(expand = 1, fill ="both")
    app.subTabControlTrendyol.pack(expand=1, fill="both")
    app.subTabControlGetir.pack(expand=1, fill="both")
    app.subTabControlGetirBuyuk.pack(expand = 1, fill ="both")
    app.getCategoryListTrendyol()
    app.getCategoryListGetir()
    app.getCategoryListGetirBuyuk()
    app.pageIndexTrendyol.current(0)
    app.pageIndexGetir.current(0)
    app.pageIndexGetirBuyuk.current(0)
    app.tabControl.bind('<<NotebookTabChanged>>', app.on_tab_change)
    app.subTabControlTrendyol.bind('<<NotebookTabChanged>>', app.on_Trendyol_tab_change)
    app.subTabControlGetir.bind('<<NotebookTabChanged>>', app.on_Getir_tab_change)
    app.subTabControlGetirBuyuk.bind('<<NotebookTabChanged>>', app.on_GetirBuyuk_tab_change)
    root.title("Web Scraping App")
    root.geometry("490x650+100+50")
    root.resizable(1,1)
    root["bg"] = "whitesmoke"

    root.mainloop()
