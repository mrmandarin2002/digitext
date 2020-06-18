import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import window

class TextbookScanner(tk.Frame): 
    values_set = False
    current_title = ""
    current_price = 0
    current_condition = 0
    num_scanned = 0

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        self.barcode_label["text"] = "Current Barcode :" + controller.current_barcode
        if(self.values_set):
            if(controller.barcode_status == "Textbook"):
                print(controller.textbook_info)
                if(controller.textbook_info[1] == self.current_title and float(controller.textbook_info[2]) == self.current_price):
                    messagebox.showerror("Error", "This Textbook Is Already In The Database, Fool!")                        
                else: 
                    MsgOption = messagebox.askyesno("Textbook already in database!", "Would you like to replace the original values?")
                    if(MsgOption):
                        self.num_scanned += 1
                        self.textbook_label.config(text = "Number of Textbooks Scanned: " + str(self.num_scanned))
                        controller.server.delete_t(controller.current_barcode)
                        controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                        controller.update_textbook_list()
            elif(controller.barcode_status == "Student"):
                messagebox.showwarning("Warning!", "You are scanning in a student's barcode ID!")
            else:
                self.num_scanned += 1
                self.barcode_label.config(text = "Current Barcode: " + controller.current_barcode)
                self.textbook_label.config(text = "Number of Textbooks Scanned: " + str(self.num_scanned))
                self.current_condition = controller.textbook_conditions_rev[self.condition_entry.get()]
                controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                controller.update_textbook_list()
        else:
            messagebox.showerror("Error", "Please set the values before scanning in a barcode")

    def check_similarity(self, textbook_check, textbook_list):
        similar_list = []
        check_arr = [0] * 128
        char_list = []
        for x in range(0, len(textbook_check)):
            if(ord(textbook_check[x]) not in char_list):
                char_list.append(ord(textbook_check[x]))
            check_arr[ord(textbook_check[x])] += 1
        for textbook in textbook_list:
            temp_check_arr = check_arr
            for x in range(0, len(textbook)):
                temp_check_arr[ord(textbook[x])] -= 1
            tot_sum = 0
            for num in char_list:
                tot_sum += temp_check_arr[num]
            if(abs(tot_sum + abs(len(textbook) - len(textbook_check))) < ((len(textbook) + len(textbook_check) / 2) * 0.15)):
                similar_list.append(textbook)
        return similar_list

    def set_values(self, controller):
        if(self.values_set):
            self.set_button.config(text = "SET VALUES")
            self.title_entry.config(state = "normal")
            self.price_entry.config(state = "normal")
            self.textbook_label.config(text = "Number of Textbooks Scanned:")
            self.num_scanned = 0
            self.values_set = False
        else:
            price_string = self.price_entry.get()
            try:
                similar_list = self.check_similarity(self.title_entry.get(), controller.scanner.textbook_list)
                print(similar_list)
                self.current_price = float(price_string)
                self.current_title = self.title_entry.get()
                self.set_button.config(text = "RESET")
                self.textbook_label.config(text = "Number of Textbooks Scanned: " + str(self.num_scanned))
                self.title_entry.config(state = "disabled")
                self.price_entry.config(state = "disabled")
                self.values_set = True
            except ValueError:
                messagebox.showerror("Error", "Please Make Sure That The Price Is Actually A Number, Idiot.")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TextbookScanner.configure(self, background = controller.MAROON)
        
        #labels
        main_label = tk.Label(self, text="Add Textbooks", font = controller.TITLE_FONT, bg = controller.MAROON)
        main_label.grid(row = 0, column = 0, padx = (95,0))
        title_label = tk.Label(self, text = "Title:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        title_label.grid(row = 1, column = 0, padx = 10, pady = (20, 0), sticky = "W")
        condition_label = tk.Label(self, text = "Condition:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        condition_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "W")
        price_label = tk.Label(self, text = "Price:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        price_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = "W")
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_label.grid(row = 3, column = 0, padx= (290,0) , pady = (20,0), sticky = "W")
        self.textbook_label = tk.Label(self, text = "Number of Textbooks Scanned: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_label.grid(row = 4, column = 0, padx = (290, 0), sticky = "W")

        #buttons
        manual_entry = tk.Button(self, text = "Manual Barcode Entry", font = controller.MENU_FONT, command = lambda: window.manual_barcode_entry_window(self, controller).show(controller))
        manual_entry.grid(row = 8, column = 0, padx = 10, pady = (20, 0), sticky = "W")
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 9, column = 0, padx = 10, pady = (100,0), sticky = "W")
        self.set_button = tk.Button(self, text = "Set Values", command = lambda : self.set_values(controller = controller), font = controller.BUTTON_FONT)
        self.set_button.grid(row = 7, column = 0, padx = 10, pady = 10, sticky = "W")

        #entry points
        self.title_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.title_entry.grid(row = 2, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.price_entry = tk.Entry(self, font = controller.FIELD_FONT)
        self.price_entry.grid(row = 6, column = 0, padx = 10, pady = (0,10), sticky = "W")
        self.condition_choices = ["New", "Good", "Fair", "Poor", "Destroyed"]
        self.condition_entry = ttk.Combobox(self, values = self.condition_choices, font = controller.FIELD_FONT, state = "readonly", width = 10)
        self.condition_entry.set("New")
        self.condition_entry.grid(row = 4, column = 0, padx = 10, pady = (0,10), sticky = "W")
