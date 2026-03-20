import tkinter as tk

############################# MAIN MENU #################################

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)        ## Call init on tk.Frame to register with the parent ##
        buttons = ["Inventory", "Sales", "Reports", "Settings"]

        # Create a 2x2 grid of big buttons
        for i, name in enumerate(buttons):
            btn = tk.Button(self, text=name, font=("Arial", 24), 
                            command=lambda n=name: controller.show_page(n))
            btn.grid(row=i//2, column=i%2, sticky="nsew", padx=20, pady=20)

        # Make the grid responsive
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)

        for row in range(2):
            self.grid_rowconfigure(row, weight=1)
       


