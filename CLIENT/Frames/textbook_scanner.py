import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from playsound import playsound

import window, time

class TextbookScanner(tk.Frame): 
    values_set = False
    current_title = ""
    current_price = 0
    current_condition = 0
    num_scanned = 0
    textbook_deletion_mode = False
    num_of_deleted_textbooks = 0

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        print("TEXTBOOKSCANNER BARCODE")
        self.barcode_label["text"] = "Current Barcode :" + controller.current_barcode
        self.barcode_label.config(text = "Current Barcode: " + controller.current_barcode)
        if(not self.textbook_deletion_mode):
            if(self.values_set):
                if(controller.barcode_status == "Textbook"):
                    print(controller.textbook_info)
                    if(controller.textbook_info[1] == self.current_title and float(controller.textbook_info[2]) == self.current_price):
                        messagebox.showerror("Error", "This Textbook Is Already In The Database, Fool!")                        
                    else: 
                        if(messagebox.askyesno("Textbook Already In Database!", "Would You Like To Replace: " + controller.textbook_info[1] + "?")):
                            self.num_scanned += 1
                            self.textbook_label.config(text = "Number of Textbooks Scanned: " + str(self.num_scanned))
                            controller.server.delete_t(controller.current_barcode)
                            controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                            controller.update_textbook_list()
                elif(controller.barcode_status == "Student"):
                    messagebox.showwarning("Warning!", "You Are Scanning In " + controller.student_info[2] + "'s barcode ID! Please Add Textbooks, We Have Enough Students At This School")
                else:
                    self.current_condition = controller.textbook_conditions_rev[self.condition_entry.get()]
                    controller.server.add_t(controller.current_barcode, self.current_title, str(self.current_price), str(self.current_condition))
                    controller.update_textbook_list()
                    try:
                        playsound("Textbook_Scan_In_Sound.mp3", block = False)
                    except:
                        print("no sound :(")
                    self.num_scanned += 1
                    self.textbook_label.config(text = "Number of Textbooks Scanned: " + str(self.num_scanned))
            else:
                messagebox.showerror("Error", "Please Set The Values Before Scanning In A Barcode")
        else:
            if(controller.barcode_status == "Textbook"):
                controller.server.delete_t(controller.current_barcode)
                self.num_of_deleted_textbooks += 1
                self.textbook_label["text"] = "Number Of Textbooks Deleted: " + str(self.num_of_deleted_textbooks)
            else:
                print("Cannot Delete This As It Is Not In The Database, Baka")
 
    #not efficient enough
    def check_similarity(self, textbook_check, textbook_list):
        answer = []
        start_time = time.time()
        textbook_check = textbook_check.replace('-', ' ')
        textbook_check = textbook_check.replace(',', ' ')
        check_list = textbook_check.split(' ')
        check_list = [i.replace(' ', '').lower() for i in check_list]
        print(check_list)
        for textbook in textbook_list:
            cnt = 0
            cur_textbook_check = textbook.replace('-', ' ')
            cur_textbook_check = cur_textbook_check.replace(',', ' ')
            cur_check_list = cur_textbook_check.split(' ')
            cur_check_list = [i.replace(' ', '').lower() for i in cur_check_list]
            for word in check_list:
                if(word in cur_check_list):
                    cnt += 1
            if(cnt >= min(len(cur_check_list), len(check_list))):
                answer.append(textbook)
            
        print("Check_similarity Runtime")
        print("--- %s seconds ---" % (time.time() - start_time))
        return answer

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
                self.textbook_label.config(text = "Number Of Textbooks Scanned: " + str(self.num_scanned))
                self.title_entry.config(state = "disabled")
                self.price_entry.config(state = "disabled")
                self.values_set = True
            except ValueError:
                messagebox.showerror("Error", "Please Make Sure That The Price Is Actually A Number, Idiot.")

    def switch_textbook_deletion_mode(self):
        if(self.textbook_deletion_mode):
            self.textbook_label["text"] = "Number Of Textbooks Scanned: "
            self.num_of_deleted_textbooks = 0
            self.title_entry.config(state = "normal")
            self.price_entry.config(state = "normal")
            self.condition_entry.config(state = "readonly")
            self.main_label["text"] = "Add Textbooks"
            self.delete_textbook_button["text"] = "Delete Textbook Button"
        else:
            self.textbook_label["text"] = "Number Of Textbooks Deleted: " + str(self.num_of_deleted_textbooks)
            try:
                playsound("Delete_Textbook_Warning.mp3", block = False)
            except:
                print("no sound :(")
            messagebox.showwarning("DANGER DANGER!", "YOU ARE ENTERING TEXTBOOK DELETION MODE. BE CAREFUL WITH YOUR POWER!")
            self.title_entry.config(state = "disabled")
            self.price_entry.config(state = "disabled")
            self.condition_entry.config(state = "disabled")
            self.delete_textbook_button["text"] = "Revert Back To Add Textbook Mode"
            self.main_label["text"] = "TEXTBOOK DELETION MODE"
        self.textbook_deletion_mode = not self.textbook_deletion_mode

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TextbookScanner.configure(self, background = controller.MAROON)
        
        #labels
        self.main_label = tk.Label(self, text="Add Textbooks", font = controller.TITLE_FONT, bg = controller.MAROON)
        self.main_label.grid(row = 0, column = 0, padx = (95,0))
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
        self.delete_textbook_button = tk.Button(self, text = "Delete Textbook Button", font = controller.MENU_FONT, command = self.switch_textbook_deletion_mode)
        self.delete_textbook_button.grid(row = 9, column = 0, padx = 10, pady = (10, 0), sticky = "W")

        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 10, column = 0, padx = 10, pady = (50,0), sticky = "W")
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
