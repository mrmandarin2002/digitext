#in window.py
'''
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

def get_textbook_condition(condition):
    if(condition == "New"):
        return 0
    elif(condition == "Good"):
        return 1
    elif(condition == "Fair"):
        return 2
    elif(condition == "Poor"):
        return 3
    elif(condition == "Destroyed"):
        return 4

def get_textbook_condition_rev(condition):
    condition = int(condition)
    if(condition == 0):
        return "New"
    elif(condition == 1):
        return "Good"
    elif(condition == 2):
        return "Fair"
    elif(condition == 3):
        return "Poor"
    elif(condition == 4):
        return "Destroyed"

'''