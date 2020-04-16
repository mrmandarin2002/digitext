from tkinter import *
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import sys

import interactions, font_info


class add_student_window(object):

    def add_student(self, controller):
        name = self.student_name_entry.get()
        price = self.student_deposit_label.get()
        b_id = self.student_id_entry.get()
        if(not name or not price or not b_id):
            messagebox.showerror("HUMAN ERROR", "You have not filled all the entries")
        elif(controller.server.ping()):
            try:
                price_check = float(price)
                check = True
            except:
                messagebox.showerror("CONVERSION ERROR", "Make sure that the price you've entered is a number.")
                check = False
            if(controller.server.valid_s(b_id)):
                messagebox.showerror("ERROR", "Student is already in database")
                check = False
            elif(controller.server.valid_t(b_id)):
                messagebox.showerror("ERROR", "The barcode ID is already used by a textbook")
                check = False
            if(check):
                option = messagebox.askyesno("Add Student?", "Are you sure you want to add this student?")
                if(option):
                    controller.server.add_s(student_id = str(b_id), student_name = str(name), student_deposit = str(price))

    def __init__(self, master, controller):

        popup = self.popup = Toplevel(master)
        popup.configure(background = font_info.MAROON)
        popup.title("Add Student")
        popup.iconbitmap("sphs_icon.ico")
        student_name_label = Label(popup, text = "Student Name: ", bg = font_info.MAROON, font = controller.MENU_FONT)
        student_name_label.grid(row = 0, column = 0, padx = (10,0), pady = 5, sticky = "W")
        student_id_label = Label(popup, text = "Student ID: ", bg = font_info.MAROON, font = controller.MENU_FONT)
        student_id_label.grid(row = 1, column = 0, padx = (10,0), pady = 5, sticky = "W")
        student_deposit_label = Label(popup, text = "Student Deposit: ", bg = font_info.MAROON, font = controller.MENU_FONT)
        student_deposit_label.grid(row = 2, column = 0, padx = (10,0), pady = 5, sticky = "W")
        exit_button = Button(popup, text = "Confirm Values", font = controller.MENU_FONT, command = lambda : self.add_student(controller))
        exit_button.grid(row = 3, column = 0, padx = 10, pady = 10)
        self.student_name_entry = Entry(popup, font = controller.MENU_FONT)
        self.student_name_entry.grid(row = 0, column = 1, pady = 10, padx = (0,5))
        self.student_id_entry = Entry(popup, font = controller.MENU_FONT)
        self.student_id_entry.grid(row = 1, column = 1,  pady = 10, padx = (0,5))
        self.student_deposit_label = Entry(popup, font = controller.MENU_FONT)
        self.student_deposit_label.grid(row = 2, column = 1,  pady = 10, padx = (0,5))

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
        self.configure(background = font_info.MAROON)
        self.title("Add Textbook")
        self.iconbitmap("sphs_icon.ico")
        self.textbook_name = tk.StringVar()
        title_label = tk.Label(self, text = "Enter the name of the textbook:", font = controller.MENU_FONT, bg = font_info.MAROON)
        title_label.grid(row = 0, column = 0,padx = 5, pady = 5)
        self.textbook_entry = tk.Entry(self)
        self.textbook_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        textbook_button = tk.Button(self, text = "Search textbook", font = controller.BUTTON_FONT, command = lambda : self.search_textbook(controller))
        textbook_button.grid(row = 2, column = 0, padx = 5, pady = 5)
        pot_textbook_label = tk.Label(self, text = "Potential Textbooks:", font = controller.MENU_FONT, bg = font_info.MAROON)
        pot_textbook_label.grid(row = 3, column = 0, padx = 5, pady = (10, 0))
        self.textbook_list = tk.Listbox(self, bd = 0, bg = font_info.MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = font_info.MAROON)
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
        self.TITLE_FONT = tkfont.Font(family=font_info.MAIN_FONT, size=20, weight="bold")
        self.SUBTITLE_FONT = tkfont.Font(family = font_info.MAIN_FONT, size = 14, weight = "bold")
        self.FIELD_FONT = tkfont.Font(family = font_info.MAIN_FONT, size = 11)
        self.BUTTON_FONT = tkfont.Font(family=font_info.MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = font_info.MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family=font_info.MAIN_FONT, size=11)
        self.configure(background = font_info.MAROON)
        self.title("Condition of Textbook?")
        title_label = tk.Label(self, text = "What is the current condition of this textbook?", font = self.MENU_FONT, bg = font_info.MAROON)
        title_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.condition_choices = ["New", "Good", "Fair", "Poor", "Destroyed"]
        self.condition_entry = ttk.Combobox(self, values = self.condition_choices, font = self.FIELD_FONT, state = "readonly", width = 10)
        self.condition_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
        confirm_button = tk.Button(self, text = "Confirm Condition", font = self.BUTTON_FONT, command = self.death)
        confirm_button.grid(row = 3, column = 0, padx = 5, pady = (0, 10))

    def death(self, event = None):
        self.condition.set(self.condition_entry.get())
        self.destroy()

    def show(self):
        self.wait_window()
        return self.condition.get()