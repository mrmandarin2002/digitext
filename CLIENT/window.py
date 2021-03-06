from tkinter import *
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import sys

MAIN_FONT = "Helvetica"
MAROON = '#DFF9FB'
PINK = '#FF00D4'
NEON_GREEN = '#4DFF4D'
WHITE = (255,255,255)
BLACK = (0,0,0)

class add_textbook_window(tk.Toplevel):

    current_textbook_list = []

    def search_textbook(self, controller):
        self.entered_textbook = self.textbook_entry.get()
        self.entered_textbook.replace("-", " ")
        self.entered_textbook.replace(",", " ")
        textbook_words = self.entered_textbook.split()
        self.current_textbook_list.clear()
        self.textbook_list.delete(0, tk.END)
        cnt = 0 
        print(textbook_words)
        for textbook in controller.scanner.textbook_list:
            print("TEXTBOOK:", textbook)
            check = True
            for keyword in textbook_words:
                if(keyword.lower() not in textbook.lower()):
                    check = False
                    break
            if(check):
                self.current_textbook_list.append(textbook)
                self.textbook_list.insert(cnt, textbook)
                cnt += 1

    def select_textbook(self,event, controller):
        self.textbook_name.set(self.textbook_list.get(self.textbook_list.curselection()))

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.configure(background = MAROON)
        self.title("Add Textbook")
        self.iconbitmap("sphs_icon.ico")
        self.textbook_name = tk.StringVar()
        title_label = tk.Label(self, text = "Enter Textbook Name:", font = controller.MENU_FONT, bg = MAROON)
        title_label.grid(row = 0, column = 0,padx = 5, pady = 5)
        self.textbook_entry = tk.Entry(self)
        self.textbook_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        textbook_button = tk.Button(self, text = "Search Textbook", font = controller.BUTTON_FONT, command = lambda : self.search_textbook(controller))
        textbook_button.grid(row = 2, column = 0, padx = 5, pady = 5)
        pot_textbook_label = tk.Label(self, text = "Potential Textbooks:", font = controller.MENU_FONT, bg = MAROON)
        pot_textbook_label.grid(row = 3, column = 0, padx = 5, pady = (10, 0))
        self.textbook_list = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
        self.textbook_list.grid(row = 4, column = 0, padx = 5, pady = (0, 10))
        self.textbook_list.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))
        confirm_button = tk.Button(self, text = "Add Textbook", font = controller.BUTTON_FONT, command = self.death)
        confirm_button.grid(row = 5, column = 0, padx = 5, pady = (0, 10))

    def death(self, event=None):
        self.destroy()    

    def show(self):
        self.wait_window()
        return self.textbook_name.get()

class price_window(tk.Toplevel):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.condition = tk.StringVar()
        self.TITLE_FONT = tkfont.Font(family=MAIN_FONT, size=20, weight="bold")
        self.SUBTITLE_FONT = tkfont.Font(family = MAIN_FONT, size = 13, weight = "bold")
        self.FIELD_FONT = tkfont.Font(family = MAIN_FONT, size = 11)
        self.BUTTON_FONT = tkfont.Font(family=MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family=MAIN_FONT, size=11)
        self.ENTRY_FONT = tkfont.Font(family = MAIN_FONT, size =13)
        self.configure(background = MAROON)
        self.title("Condition of Textbook?")
        title_label = tk.Label(self, text = "What is the current condition of this textbook?", font = self.SUBTITLE_FONT, bg = MAROON)
        title_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.condition_choices = ["New", "Good", "Fair", "Poor", "Destroyed"]
        self.condition_entry = ttk.Combobox(self, values = self.condition_choices, font = self.ENTRY_FONT, state = "readonly", width = 10)
        self.current_idx = int(controller.textbook_info[3])
        self.condition_entry.current(self.current_idx)
        self.condition_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.condition_entry.focus_set()
        confirm_button = tk.Button(self, text = "Confirm Condition", font = self.BUTTON_FONT, command = self.death)
        confirm_button.grid(row = 3, column = 0, padx = 5, pady = (0, 10))
        self.bind('<Return>', self.death)
        self.focus_force()

    def death(self, event = None):
        self.condition.set(self.condition_entry.get())
        self.destroy()

    def show(self):
        self.wait_window()
        return self.condition.get()

class manual_barcode_entry_window(tk.Toplevel):
    
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.configure(background = MAROON)
        self.title("Add Textbook")
        self.barcode = tk.StringVar()
        title_label = tk.Label(self, text = "Enter Barcode:", font = controller.MENU_FONT, bg = MAROON)
        title_label.grid(row = 0, column = 0,padx = (25,25), pady = 8)
        self.textbook_entry = tk.Entry(self, font = controller.MENU_FONT)
        self.textbook_entry.grid(row = 1, column = 0, padx = (15,15), pady = 5)
        self.textbook_entry.focus_set()
        confirm_button = tk.Button(self, text = "Confirm Barcode", font = controller.BUTTON_FONT, command = self.death)
        confirm_button.grid(row = 2, column = 0, padx = 5, pady = (0, 10))
        self.bind('<Return>', self.death)

    def death(self, event=None):
        self.barcode.set(self.textbook_entry.get())
        self.destroy()    

    def show(self, controller):
        self.wait_window()
        controller.scanner.current_barcode = str(self.barcode.get())
        controller.scanner.check_barcode(controller)
        print(controller.scanner.current_barcode)

class ip_config_window(tk.Toplevel):
    
    def __init__(self,  controller):
        tk.Toplevel.__init__(self, controller)
        self.configure(background = MAROON)
        self.title("IP Config")
        self.ip = tk.StringVar()
        title_label = tk.Label(self, text = "Enter Server's IP Address:", font = controller.MENU_FONT, bg = MAROON)
        title_label.grid(row = 0, column = 0,padx = (15,15), pady = 5)
        self.textbook_entry = tk.Entry(self)
        self.textbook_entry.grid(row = 1, column = 0, padx = (15,15), pady = 5)
        confirm_button = tk.Button(self, text = "Confirm IP Address", font = controller.BUTTON_FONT, command = self.death)
        confirm_button.grid(row = 2, column = 0, padx = 5, pady = (0, 10))

    def death(self, event=None):
        self.ip.set(self.textbook_entry.get())
        self.destroy()    

    def show(self, controller):
        self.wait_window()
        controller.ip_address = str(self.ip.get())


class merge_textbook_window(tk.Toplevel):

    current_textbook_list = []
    selected_textbook_name = ""
    textbook_selected = False

    def search_textbook(self, controller):
        self.controller.scanner.update_textbook_list()
        self.entered_textbook = self.textbook_entry.get()
        self.entered_textbook.replace("-", " ")
        self.entered_textbook.replace(",", " ")
        textbook_words = self.entered_textbook.split()
        self.current_textbook_list.clear()
        self.textbook_list.delete(0, tk.END)
        print(textbook_words)
        for textbook in controller.scanner.textbook_list:
            print("TEXTBOOK:", textbook)
            check = True
            for keyword in textbook_words:
                if(keyword.lower() not in textbook.lower()):
                    check = False
                    break
            if(check and textbook != self.selected_textbook_name):
                self.current_textbook_list.append(textbook)
        self.current_textbook_list.sort()
        cnt = 0 
        for textbook in self.current_textbook_list:
            self.textbook_list.insert(cnt, textbook)
            cnt += 1
                

    def select_textbook(self,event, controller):
        self.textbook_name.set(self.textbook_list.get(self.textbook_list.curselection()))
        if(self.textbook_selected):
            self.confirm_button["text"] = "Confirm That You Would Like To Replace " + self.selected_textbook_name + " with " + self.textbook_name.get()

    def merge_textbook(self):
        if(self.textbook_name.get()):
            if(not self.textbook_selected):
                self.selected_textbook_name = self.textbook_name.get()
                self.textbook_list.delete(0, END)
                self.confirm_button["text"] = "Confirm That You Would Like To Replace " + self.selected_textbook_name + " with " + " "
                self.textbook_name.set('')
            else:
                if(self.textbook_name.get()):
                    self.controller.scanner.server.merge_textbooks(self.selected_textbook_name, self.textbook_name.get())
                    self.textbook_list.delete(0, END)
                    print("Replaced " + self.selected_textbook_name + " with + " + self.textbook_name.get())
                    self.confirm_button["text"] = "Replace Values With"
        else:
            print("ERROR: Please Select A Textbook First")
        self.textbook_selected = not self.textbook_selected

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.controller = controller
        self.configure(background = MAROON)
        self.title("Add Textbook")
        self.iconbitmap("sphs_icon.ico")
        self.textbook_name = tk.StringVar()
        self.title_label = tk.Label(self, text = "Enter Textbook Name:", font = controller.MENU_FONT, bg = MAROON)
        self.title_label.grid(row = 0, column = 0,padx = 5, pady = 5)
        self.textbook_entry = tk.Entry(self)
        self.textbook_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.textbook_button = tk.Button(self, text = "Search Textbook", font = controller.BUTTON_FONT, command = lambda : self.search_textbook(controller))
        self.textbook_button.grid(row = 2, column = 0, padx = 5, pady = 5)
        self.pot_textbook_label = tk.Label(self, text = "Potential Textbooks:", font = controller.MENU_FONT, bg = MAROON)
        self.pot_textbook_label.grid(row = 3, column = 0, padx = 5, pady = (10, 0))
        self.textbook_list = tk.Listbox(self, bd = 0, bg = MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = MAROON)
        self.textbook_list.grid(row = 4, column = 0, padx = 5, pady = (0, 10))
        self.textbook_list["width"] = 50
        self.textbook_list.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))
        self.confirm_button = tk.Button(self, text = "Replace Values With", font = controller.BUTTON_FONT, command = self.merge_textbook)
        self.confirm_button.grid(row = 5, column = 0, padx = 5, pady = (0, 10))

    def death(self, event=None):
        self.destroy()    

    def show(self, controller):
        self.wait_window()
        return self.textbook_name.get()

