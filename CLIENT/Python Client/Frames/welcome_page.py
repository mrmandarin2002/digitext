import tkinter as tk


#welcome screen, no need to explain
class WelcomePage(tk.Frame):

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass

    def can_enter(self, controller):
        controller.check_requisites = True
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        WelcomePage.configure(self, background = controller.MAROON)
        welcome_title = tk.Label(self, text = "Welcome to DigiText!!", font = controller.TITLE_FONT , bg = controller.MAROON)
        welcome_title.pack(side = "top", pady = 150, padx = 50)
        welcome_button = controller.make_button(controller = self, d_text = "Press to continue...", scene = "Menu", option = '')
        welcome_button.pack()
