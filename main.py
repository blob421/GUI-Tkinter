import tkinter as tk
from screens.inventory import Inventory
from screens.main_menu import MainMenu
from screens.top_bar import Top_bar
import os 
############################ ROOT (Main Screen) ###############################

icon_path = os.path.join(os.path.dirname(__file__), 'assets', "favicon2.ico")

root = tk.Tk()      
root.title("Main Menu")
root.iconbitmap(icon_path)
root.state("zoomed")

#root.geometry(""400x400) Initial size
root.minsize(800,400)


########################### APP CONTROLLER ########################
class App:
    def __init__(self, root):
        self.root = root                          ### Register root to change screen name ###
        self.container = tk.Frame(root)
  
        self.container.pack(fill="both", expand=True)
        self.topbar = Top_bar(self.container, self)
        self.topbar.place(relwidth=1, relheight=0.05, rely=0.01)
        self.pages = {}

        # Register pages
        self.pages["Main Menu"] = MainMenu(self.container, self)
        self.pages['Inventory'] = Inventory(self.container, self)
        # Add more pages here...

        # Place all pages in the same spot
        for page in self.pages.values():
            page.place(relwidth=1, relheight=0.95, rely=0.05)   ### Make them take full size of the container

        self.show_page("Main Menu")

    def show_page(self, name):
        page = self.pages[name]
        self.root.title(name)
        page.lift()



app = App(root)                                   ### Instantiate controller ####
root.mainloop()