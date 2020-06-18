import tkinter as tk

#menu, basically a window where you can go into the more important frames   
class Menu(tk.Frame):

    def clear(self):
        pass
    
    def barcode_scanned(self, controller):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Menu.configure(self, background = controller.MAROON)
        menu_title = tk.Label(self, text = "DigiText Menu", font = controller.TITLE_FONT , bg = controller.MAROON)
        menu_title.pack(pady = (100, 0))
        controller.make_back_button(self).pack(pady = (200, 0))