import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
                if(controller.textbook_info[1] == self.current_title and float(controller.textbook_info[2]) == self.current_price):
                    messagebox.showerror("Error", "This textbook has the same values as the set values")                        
                else: 
                    MsgOption = messagebox.askyesno("Textbook already in database!", "Would you like to replace the original values?")
                    if(MsgOption):
                        self.num_scanned += 1
                        self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                        controller.server.delete_t(controller.current_barcode)
                        controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                        controller.update_textbook_list()
            elif(controller.barcode_status == "Student"):
                messagebox.showwarning("Warning!", "You are scanning in a student's barcode ID!")
            else:
                self.num_scanned += 1
                self.barcode_label.config(text = "Current Barcode: " + controller.current_barcode)
                self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                self.current_condition = controller.textbook_conditions_rev[self.condition_entry.get()]
                controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                controller.update_textbook_list()
        else:
            messagebox.showerror("Error", "Please set the values before scanning in a barcode")

    def check_similarity(self, textbook_check, textbook_list):
        similar_list = []
        og_tc = textbook_check
        for textbook in textbook_list:
            og_t = textbook
            textbook_check = og_tc
            if(textbook != textbook_check):
                if(textbook.lower() == textbook_check.lower()):
                    similar_list.append(textbook)
                else:
                    textbook = textbook.lower()
                    textbook_check = textbook_check.lower()
                    textbook.replace('-',' ')
                    textbook.replace('.',' ')
                    textbook.replace('_',' ')
                    textbook_check.replace('-',' ')
                    textbook_check.replace('.',' ')
                    textbook_check.replace('_',' ')
                    t_list = textbook.split()
                    t_list2 = textbook_check.split()
                    length1 = len(t_list)
                    length2 = len(t_list2)
                    cnt = 0.0
                    for x in range(0, min(length1, length2)):
                        if(t_list[x] == t_list2[x]):
                            cnt += 1.0
                        elif(''.join(sorted(t_list[x])) == ''.join(sorted(t_list2[x]))):
                            cnt += 1.0
                    if((float(cnt / max(length1, length2))) > 0.5):
                        similar_list.append(og_t)
        return similar_list

    def set_values(self, controller):
        if(self.values_set):
            self.set_button.config(text = "SET VALUES")
            self.title_entry.config(state = "normal")
            self.price_entry.config(state = "normal")
            self.textbook_label.config(text = "Number of textbooks scanned:")
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
                self.textbook_label.config(text = "Number of textbooks scanned: " + str(self.num_scanned))
                self.title_entry.config(state = "disabled")
                self.price_entry.config(state = "disabled")
                self.values_set = True
            except ValueError:
                messagebox.showerror("Error", "Please make sure that the price is actually a number")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TextbookScanner.configure(self, background = controller.MAROON)
        
        #labels
        main_label = tk.Label(self, text="Textbook Scanner", font = controller.TITLE_FONT, bg = controller.MAROON)
        main_label.grid(row = 0, column = 0, padx = (95,0))
        title_label = tk.Label(self, text = "Title:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        title_label.grid(row = 1, column = 0, padx = 10, pady = (20, 0), sticky = "W")
        condition_label = tk.Label(self, text = "Condition:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        condition_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "W")
        price_label = tk.Label(self, text = "Price:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        price_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = "W")
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_label.grid(row = 3, column = 0, padx= (290,0) , pady = (20,0), sticky = "W")
        self.textbook_label = tk.Label(self, text = "Number of textbooks scanned: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_label.grid(row = 4, column = 0, padx = (290, 0), sticky = "W")

        #buttons
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 8, column = 0, padx = 10, pady = (150,0), sticky = "W")
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
