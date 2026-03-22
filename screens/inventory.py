import tkinter as tk
from tkinter import ttk
import psycopg

categories = ["Fruit","Vegetables","Dairy","Meat","Seafood","Bakery","Frozen Foods","Snacks",
    "Beverages","Canned Goods","Condiments","Spices & Herbs"]

db_uri = "postgresql://postgres:1246@localhost:5432/TkinterGui"
small_font = ("Arial", 13)
xs_font = ('Arial', 12)

class Inventory_search_input(tk.Entry):

    def __init__(self, master, font, textvariable):
        super().__init__(master, font=font, textvariable=textvariable)

      
        self.placeholder_text = 'Search Here'
        self.placeholder_color = 'grey'

        self.default_fg = self["fg"]                                ### DEFAULT BLACK COLOR ###

        self.bind('<FocusIn>', self.clear_placeholder)
        self.bind('<FocusOut>', self.add_placeholder)
        self.add_placeholder()

    def clear_placeholder(self, *args, **kwargs):
       if self.get() and self.get() == 'Search Here':
          self.delete(0, "end")
          self["fg"] = self.default_fg

    def add_placeholder(self, *args, **kwargs):
       if not self.get():
            self["fg"] = self.placeholder_color
            self.insert(0, self.placeholder_text)

############################ INVENTORY ############################
class Inventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  
                                                                   ### Register child ###
        self.current_db_table = 'fruits'
        container = tk.Frame(self)                                 ### Outer container 
        container.pack(fill='both', expand=True)
        

        left_container = tk.Frame(container, bg='#555555')       ### Left and right containers
        left_container.pack(side="left", fill="y", ipadx=10)
       

        right_container = tk.Frame(container)
        right_container.pack(side="right", fill="both", expand=True)
        
        #-------------- Left container -------------------
        left_head_title = tk.Label(left_container, text="Edit your Product", bg="#555555", fg="white",
                font=("Arial", 16))
        
        left_head_title.pack(fill='x', pady=15, padx=10)

        self.product_id_var = tk.IntVar()
       
        product_name_label = tk.Label(left_container, text="Product name", font=small_font)
        product_name_label.pack(pady=10)

        self.product_name_var = tk.StringVar()
        self.product_name_input = tk.Entry(left_container, font=small_font, textvariable=self.product_name_var)
        self.product_name_input.pack(fill="x", padx=30, pady=10, ipady=5)


        product_count_label = tk.Label(left_container, font=small_font, text="Inventory count")
        product_count_label.pack(pady=10)
        self.quantity_var = tk.IntVar(value=0)
        product_count_input = tk.Spinbox(left_container, to=999999, from_=0, increment=1, 
                                         textvariable=self.quantity_var, font=small_font)
        product_count_input.pack(fill='x', pady=10, padx=30)


        product_category_label = tk.Label(left_container, font=small_font, text="Product category")
        product_category_label.pack(pady=10)

        self.category_var = tk.StringVar()
        self.category_box = ttk.Combobox(left_container,
            textvariable=self.category_var,
            values=categories,
            state="readonly",   # prevents typing random text
            font=("Arial", 13)
        )
        self.category_box.pack(fill="x", padx=30, pady=10)


        confirm_edit_btn = tk.Button(left_container,text='Save modifications', 
                                                    command=self.save_product_edit)
        confirm_edit_btn.pack(side="bottom", pady=20, anchor="center")
  
        #-------------- Right container ------------------
        
        search_frame = tk.Frame(right_container)                   ### Unique frame for seach ###
        search_frame.pack(fill="x", padx=20, pady=10)


        self.textvar = tk.StringVar()
        self.textvar.trace_add("write", self.search_db_with_search)

        self.search_bar = Inventory_search_input(search_frame, font=small_font, textvariable=self.textvar, )
        self.search_bar.pack(fill="x", expand=True)



        list_frame = tk.Frame(right_container)   
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(list_frame)                         #--- Scrollbar ---
        scrollbar.pack(side="right", fill="y")
 


        table_columns = ('Id', 'Name', 'Quantity', 'Product_type')   # --- Product Table ---
        self.item_list = ttk.Treeview(
            list_frame,
           
            yscrollcommand=scrollbar.set, columns=table_columns, show="headings"
        )
        self.item_list.heading('Id', text='Id')
        self.item_list.heading('Name', text='Name')
        self.item_list.heading('Quantity', text='Quantity')
        self.item_list.heading('Product_type', text='Product_type')
        self.item_list.column('Id', anchor='center')
        self.item_list.column('Quantity', anchor='center')
        self.item_list.pack(fill="both", expand=True)
        self.item_list.bind("<<TreeviewSelect>>", self.on_item_select) # ---


        scrollbar.config(command=self.item_list.yview)
        self.init_products_results()            

    def on_item_select(self, event):
         tree = event.widget
  
         selection = tree.selection()
         if not selection:
            return
         index = selection[0]
         selected_row = tree.item(index, "values")
        
         
         self.product_id_var.set(selected_row[0])
         self.product_name_var.set(selected_row[1])

         self.quantity_var.set(selected_row[2])
         self.category_var.set(selected_row[3])



    def save_product_edit(self):
        db_query = f"""UPDATE {self.current_db_table} SET name= %s, quantity = %s, product_type = %s 
                                                WHERE id = %s"""
        try:
            with psycopg.connect(db_uri) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(db_query, (self.product_name_var.get(), self.quantity_var.get(), 
                                            self.category_var.get(), self.product_id_var.get()))
        except psycopg.Error as e:
            print(e)

    def search_db_with_search(self, *args, **kwargs):
        if not hasattr(self, 'search_bar'):
            return 
        
        elif self.textvar.get() != "" and self.textvar.get() != "Search Here":
            for item in self.item_list.get_children():
                 self.item_list.delete(item)
        
        elif self.search_bar.get() == '' or self.search_bar.get() == 'Search Here':
            if not self.item_list.get_children():
                self.init_products_results()
            return
        try:
            with psycopg.connect(db_uri) as conn:
                with conn.cursor() as cursor: 
                    cursor.execute(
                    rf"SELECT * FROM {self.current_db_table} WHERE name %% %s ORDER BY similarity(name, %s) DESC",
                    (self.textvar.get(), self.textvar.get())
                )
                    rows = cursor.fetchmany(20)
                    for r in rows:
                      self.item_list.insert("","end", values= (r[0], r[1], r[2], r[3]))

        except psycopg.Error as e:
            print(e)

    def init_products_results(self):
        with psycopg.connect(db_uri) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.current_db_table} ORDER BY id ASC LIMIT 30")
                rows = cur.fetchall()
                if(rows):
                    for r in rows:
                        self.item_list.insert("","end", values= (r[0], r[1], r[2], r[3]))