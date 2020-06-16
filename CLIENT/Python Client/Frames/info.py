import tkinter as tk
from tkinter import messagebox 

class Info(tk.Frame):

    textbook_selected = False
    textbook_selected_index = 0
    textbook_list_made = False

    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_name_label.config(text = "Student Name: ")
        self.textbook_barcode_label["text"] = "Textbook Barcode: "
        if(self.textbook_list_made):
            self.textbook_list_made = False
            self.textbook_list.delete(0, tk.END)
            self.textbook_list.grid_forget()

    def select_textbook(self, event, controller):
        self.textbook_selected = True
        self.textbook_selected_index = int((self.textbook_list.curselection())[0])
        controller.textbook_info = controller.server.info_t(controller.student_textbooks[self.textbook_selected_index])
        self.display_textbook_info(controller)

    def display_textbook_info(self, controller):
        self.textbook_title_label["text"] = "Textbook Title: " + controller.textbook_info[1]
        self.textbook_condition_label["text"] = "Textbook Condition: " + controller.textbook_conditions[int(controller.textbook_info[3])]
        self.textbook_price_label["text"] = "Textbook Price: " + controller.textbook_info[2]
        self.textbook_barcode_label["text"] = "Textbook Barcode " + controller.textbook_info[0]

    def barcode_scanned(self, controller):
        self.textbook_selected = False
        if(controller.barcode_status == "Student"):
            self.clear()
            self.student_name_label.config(text = "Student Name: " + controller.student_info[2])
            cnt = 1
            self.textbook_list = tk.Listbox(self, bd = 0, bg = controller.controller.MAROON, font = controller.controller.MENU_FONT, selectmode = "SINGLE", selectbackground = controller.controller.MAROON)
            for textbook in controller.student_textbooks:
                textbook_info = controller.server.info_t(textbook)
                self.textbook_list.insert(cnt, textbook_info[1])
                cnt += 1
            self.textbook_list.grid(row = 1, column = 1, sticky = "NW", rowspan = 10)
            self.textbook_list.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))

        elif(controller.barcode_status == "Textbook"):
            self.clear()
            print(controller.textbook_info[4])
            if(controller.textbook_info[4] != "None"):
                self.student_name_label["text"] = "Textbook Owner: " + controller.server.info_s(controller.textbook_info[4])[2]
            else:
                self.student_name_label["text"] = "Textbook Owner: N/A"
            self.display_textbook_info(controller)
        else:
            self.clear()
            messagebox.showerror("Fatal Error", "WTF DID YOU SCAN IN BOI????")
        self.barcode_label.config(text = "Current Barcode: " + str(controller.current_barcode))
        self.barcode_status_label["text"] = "Barcode Type: " + controller.barcode_status

    def delete_textbook(self, controller):
        if(controller.scanner.barcode_status == "Textbook"):
            controller.scanner.server.delete_t(controller.scanner.current_barcode)
            messagebox.showwarning("DELETED!", "This textbook has been deleted")
            self.clear()
        elif(self.textbook_selected):
            option = messagebox.askyesno("Warning", "Would you like to the delete (return) the textbook you selected?")
            if(option):
                controller.scanner.server.return_t(controller.textbook_info[0], 4)
                self.textbook_list.delete(self.textbook_selected_index)
                controller.scanner.student_textbooks.remove(controller.scanner.textbook_info[0])
        else:
            messagebox.showerror("ERROR", "Please select a textbook you would like to delete")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Info.configure(self, background = controller.MAROON)

        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "W")
        self.barcode_status_label = tk.Label(self, text = "Barcode Type: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_status_label.grid(row = 0, column = 0, padx = 10, pady = (50, 0), sticky = "W")
        
        textbook_info_label = tk.Label(self, text = "Textbook Info", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        textbook_info_label.grid(row = 1, column = 0, padx = 10, pady = (30, 0),  sticky = "W")
        self.textbook_title_label = tk.Label(self, text = "Textbook Title: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_title_label.grid(row = 2, column = 0, padx = 10, sticky = "W")
        self.textbook_condition_label = tk.Label(self, text = "Textbook Condition: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_condition_label.grid(row = 3, column = 0, padx = 10, sticky = "W")
        self.textbook_price_label = tk.Label(self, text = "Textbook Price: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_price_label.grid(row = 4, column = 0, padx = 10, sticky = "W")
        self.textbook_barcode_label = tk.Label(self, text = "Textbook Barcode: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_barcode_label.grid(row = 5, column = 0, padx = 10, sticky = "W")

        student_info_label = tk.Label(self, text = "Student Info", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        student_info_label.grid(row = 6, column = 0, padx = 10, pady = (20, 0),  sticky = "W")
        self.student_name_label = tk.Label(self, text = "Student Name: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.student_name_label.grid(row = 7, column = 0, padx = 10, sticky = "W")
        self.student_grade_label = tk.Label(self, text = "Student Grade: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.student_grade_label.grid(row = 8, column = 0, padx = 10, sticky = "W")
        invisible_label = tk.Label(self, text = "", bg = controller.MAROON)
        invisible_label.grid(row = 12, padx = 150)
        student_textbooks_label = tk.Label(self, text = "Student Textbooks: ", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        student_textbooks_label.grid(row = 0, column = 1, sticky = "W", pady = (30, 0))
        
        pady_dif_back = 0
        if(controller.settings["version"] == "teacher"):
            delete_button = tk.Button(self, text = "Delete Textbook", font = controller.MENU_FONT, command = lambda: self.delete_textbook(controller = controller))
            delete_button.grid(row = 9, column = 0, padx = 10, pady = (20, 0), sticky = "W")    
            pady_dif_back = 55    
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 11, column = 0, padx = 10, pady = (132 - pady_dif_back,0), sticky = "W")