import tkinter as tk
import threading

#welcome screen, no need to explain
class Stats(tk.Frame):

    in_thread = False

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass

    def can_enter(self, controller):
        controller.check_requisites = True

    def check_number(self):
        threading.Timer(1, self.check_number).start()
        if(self.controller.current_frame_name == "Stats" and not self.in_thread):
            self.in_thread = True
            self.welcome_title["text"] = "Number Of Textbooks: " + str(self.controller.scanner.get_textbook_nums())
            screen_width = self.controller.winfo_screenwidth()
            screen_height = self.controller.winfo_screenheight()
            print(screen_width, screen_height)
            self.in_thread = False
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Stats.configure(self, background = controller.MAROON)
        self.welcome_title = tk.Label(self, text = "Number Of Textbooks", font = controller.TITLE_FONT2 , bg = controller.MAROON)
        self.welcome_title.pack(side = "top", pady = 150, padx = 50)
        export_textbook_info_button = tk.Button(self, text = "Export Textbook Info", font = controller.MENU_FONT, command = controller.scanner.server.get_textbook_inventory)
        export_textbook_info_button.pack(pady = (50, 0))
        controller.make_back_button(self).pack(pady = (20, 0))
        self.check_number()