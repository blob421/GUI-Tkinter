import tkinter as tk


############################ INVENTORY ############################
class Inventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)                        ### Register child ###
        search_frame = tk.Frame(self)                   ### Unique frame for seach ###
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_bar = tk.Entry(search_frame, font=("Arial", 15))
        self.search_bar.pack(fill="x", expand=True)

        list_frame = tk.Frame(self)   
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(list_frame)                         #--- Scrollbar ---
        scrollbar.pack(side="right", fill="y")


        self.item_list = tk.Listbox(
            list_frame,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set
        )
        self.item_list.pack(fill="both", expand=True)

        scrollbar.config(command=self.item_list.yview)

        # Example items
        for i in range(50):
            self.item_list.insert("end", f"Item {i+1}")



