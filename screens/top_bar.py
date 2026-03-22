import tkinter as tk 

class Top_bar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#000000')
        self.menus = ['Navigation']
        self.menu_buttons = {}
        self.controller = controller
     

        for idx, m in enumerate(self.menus):
           btn = tk.Button(master=self, text=m, command=self.open_nav_menu)
           btn.grid(row=0, column=idx)
           self.menu_buttons[m] = btn

        self.back_button = tk.Button(master=self, text='Back', command=self.back_btn)
        self.back_button.grid(row=0, column=len(self.menu_buttons))                  # Append after menus ---

        self.contextual_menu_0 = tk.Menu(self, tearoff=0)
        self.contextual_menu_0.add_command(label='Main Menu', 
                                           command=lambda x='Main Menu': self.controller.show_page(x))

    def back_btn(self):
        if self.controller.root.title() in ['Inventory']:
            self.controller.show_page('Main Menu')

    def open_nav_menu(self):                                                        

        btn = self.menu_buttons['Navigation']
        x = btn.winfo_rootx()
        y = btn.winfo_rooty() + btn.winfo_height()
        self.contextual_menu_0.tk_popup(x, y)