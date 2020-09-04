import tkinter as tk
import window
from tkinter import messagebox

class TextbookManagement(tk.Frame):

    #checks if a student has been scanned in
    student_scanned = False
    #a variable to keep track of the student's scanned in barcode
    current_student_barcode = ""
    #whether it's return or distribution
    day = 'D'

    #Clears labels
    def clear(self):
        self.barcode_label.config(text = "Current Barcode: ")
        self.barcode_status_label.config(text = "Barcode Type: ")
        self.textbook_title_label.config(text = "Textbook Title: ")
        self.textbook_condition_label.config(text = "Textbook Condition: ")
        self.textbook_price_label.config(text = "Textbook Price: ")
        self.student_tnum_label.config(text = "Number Of Textbooks Out: ")
        self.student_name_label["text"] = "Student Name:"
        print(self.day)
        if(self.day == 'R'):
            self.mode_label["text"] = "Mode: Return"
            self.student_textbooks_label["text"] = "Textbooks Taken Out: "
        else:
            self.mode_label["text"] = "Mode: Distribution"
            self.student_textbooks_label["text"] = "Needed Textbooks: "
        self.textbook_listbox.delete(0, tk.END)
 
    #Whenever a barcode is scanned
    def barcode_scanned(self, controller):
        print("TEXTBOOKMANAGEMENT BARCODE")
        #If a student'sd barcode is scanned
        if(controller.barcode_status == "Student"):
            #this tells the program that a student's barcode is scanned and that it's ready to take in textbooks now
            self.student_scanned = True
            #makes sure to reset everything
            self.clear()
            self.barcode_label["text"] = "Current Barcode: " + controller.current_barcode
            self.student_name_label["text"] = "Student Name: " + controller.student_info[2].replace(' ', ', ')
            self.barcode_status_label.config(text = "Barcode Type: Student")
            #number of textbooks the student currently has
            self.num_of_textbooks = len(controller.student_textbooks)
            #displays the number of textbooks taken out
            self.student_tnum_label["text"] = "Number Of Textbooks Out: " + str(len(controller.student_textbooks))
            self.current_student_barcode = controller.current_barcode
            #which mode it's in
            if(self.day == 'D'):
                print(controller.student_info)
                #adds the textbooks that are assigned to the student in a list
                for cnt, textbook in enumerate(controller.student_needed_textbooks):
                    self.textbook_listbox.insert(cnt, textbook)
            else:
                #adds the textbook that are taken out by the student (or an error occurs if 0)
                if(self.num_of_textbooks):
                    for cnt, textbook in enumerate(controller.student_textbooks):
                        self.textbook_listbox.insert(cnt, controller.server.info_t(textbook)[1])
                else:
                    messagebox.showerror("ERROR", controller.student_info[2] + " has taken out no textbooks")

        elif(controller.barcode_status == "Textbook"):
            self.barcode_label["text"] = "Current Barcode: " + controller.current_barcode
            self.barcode_status_label["text"] = "Barcode Type: Textbook"
            #this is to make sure that a student has bee scanned in first
            if(self.student_scanned):
                if(self.day == 'D'):
                    #to check if the student has been assigned this textbook by a teacher
                    #if not check if he wants to take out anyways
                    for idx, textbook in enumerate(controller.student_needed_textbooks):
                        textbook_split = textbook.split(' ')
                        print("Textbook Split:")
                        print(textbook_split)
                        cur_textbook_split = controller.textbook_info[1].split(' ')
                        cur_textbook_split = [i.replace(" ", "").lower() for i in cur_textbook_split]
                        print("Current Textbook Split:")
                        print(cur_textbook_split)
                        if('Placeholder' in textbook.split(' ')):
                            textbook_split.remove('Placeholder')
                            cnt = 0
                            for word in textbook_split:
                                if(word.lower() in cur_textbook_split):
                                    cnt+= 1
                            if(cnt == len(textbook_split)):
                                controller.student_needed_textbooks[idx] = controller.textbook_info[1]
                                
                    if(controller.textbook_info[1] in controller.student_needed_textbooks or messagebox.askyesno("???", "This textbook is not needed by this student, would you like to try to assign it to him anyways?")):
                        #to check if we need to remove the textbook from the student's needed list later
                        textbook_assigned = False
                        #if the textbook is already assigned to him
                        if(controller.textbook_info[4] == self.current_student_barcode):
                            messagebox.showerror("ERROR", "This textbook is already assigned to this student")
                        #if the same type of textbook is already taken out by the student
                        elif(controller.textbook_info[1] in controller.student_textbooks_title):
                            controller.server.assign_t(controller.current_barcode, self.current_student_barcode)
                            self.num_of_textbooks += 1
                            self.student_tnum_label["text"] = "Number Of Textbooks Out: " + str(self.num_of_textbooks)
                            textbook_assigned = True
                            #messagebox.showerror("ERROR", "Student already took out a copy of " + controller.textbook_info[1] + ". He cannot own more than one type of the same textbook!")
                        #if the textbook is owned by nobody (assign)
                        elif(controller.textbook_info[4] == "None"):
                            #officially assigns textbook to student
                            controller.server.assign_t(controller.current_barcode, self.current_student_barcode)
                            self.num_of_textbooks += 1
                            self.student_tnum_label["text"] = "Number Of Textbooks Out: " + str(self.num_of_textbooks)
                            textbook_assigned = True
                        #if the textbook belongs to another student
                        else:
                            #asks if you want to replace it
                            if(messagebox.askyesno("Override?", "This textbook is already assigned to " + controller.server.info_s(controller.textbook_info[4])[2] + ". Would you like to replace anyways?")):
                                #returns the textbook to the system and then assigns it to student
                                controller.server.return_t(controller.current_barcode, controller.textbook_info[3])
                                controller.server.assign_t(controller.current_barcode, self.current_student_barcode)
                                self.num_of_textbooks += 1
                                self.student_tnum_label["text"] = "Number Of Textbooks Out: " + str(self.num_of_textbooks)
                                textbook_assigned = True
                        #this removes the student's needed textbook
                        #once the student doesn't need any more textbooks (assigned by teachers)
                        #the program shows a warning that the student has taken out all the required textbooks
                        if(textbook_assigned):
                            for x, needed_textbook in enumerate(controller.student_needed_textbooks):
                                if(controller.textbook_info[1] == needed_textbook):
                                    del controller.student_needed_textbooks[x]
                                    self.textbook_listbox.delete(x)
                                    controller.student_textbooks_title.append(controller.textbook_info[1])
                                    if(len(controller.student_needed_textbooks) == 0):
                                        messagebox.showinfo("DONE!", controller.student_info[2].replace(' ',', ') + " is done taking out his textbooks!")
                                    break
                else:
                    if(controller.textbook_info[4] == self.current_student_barcode):
                        self.num_of_textbooks -= 1
                        self.student_tnum_label["text"] = "Number Of Textbooks Out: " + str(self.num_of_textbooks)
                        self.textbook_listbox.delete(controller.student_textbooks.index(controller.current_barcode))
                        final_condition = window.price_window(self, controller).show()
                        controller.student_textbooks.remove(controller.current_barcode)
                        controller.server.return_t(controller.current_barcode, controller.textbook_conditions_rev[final_condition])
                        if(not self.num_of_textbooks):
                            messagebox.showwarning("Done!", controller.student_info[2].replace(' ', ', ') + " is done returning textbooks!")
                    elif(controller.textbook_info[4] != "None"):
                        messagebox.showerror("ERROR", "You are trying to return a textbook that belongs to " + (controller.server.info_s(controller.textbook_info[4]))[2])
                    else:
                        messagebox.showerror("ERROR", "This Textbook Is Currently Unassigned.")
            else:
                messagebox.showerror("Error", "You gotta scan in a student's barcode first my dude...")
        else:
            messagebox.showerror("Error", "I don't know what you scanned in my dude")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controlller = controller
        TextbookManagement.configure(self, background = controller.MAROON)
        
        self.barcode_label = tk.Label(self, text = "Current Barcode: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "W")
        self.barcode_status_label = tk.Label(self, text = "Barcode Type: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.barcode_status_label.grid(row = 0, column = 0, padx = 10, pady = (40, 0), sticky = "W")
        
        textbook_info_label = tk.Label(self, text = "Textbook Info", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        textbook_info_label.grid(row = 1, column = 0, padx = 10, pady = (30, 0),  sticky = "W")
        self.textbook_title_label = tk.Label(self, text = "Textbook Title: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_title_label.grid(row = 2, column = 0, padx = 10, sticky = "W")
        self.textbook_condition_label = tk.Label(self, text = "Textbook Condition: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_condition_label.grid(row = 3, column = 0, padx = 10, sticky = "W")
        self.textbook_price_label = tk.Label(self, text = "Textbook Price: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.textbook_price_label.grid(row = 4, column = 0, padx = 10, sticky = "W")

        student_info_label = tk.Label(self, text = "Student Info", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        student_info_label.grid(row = 5, column = 0, padx = 10, pady = (20, 0),  sticky = "W")
        self.student_name_label = tk.Label(self, text = "Student Name: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.student_name_label.grid(row = 6, column = 0, padx = 10, sticky = "W")
        self.student_grade_label = tk.Label(self, text = "Student Grade: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.student_grade_label.grid(row = 7, column = 0, padx = 10, sticky = "W")
        self.student_tnum_label = tk.Label(self, text = "Number Of Textbooks Out: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.student_tnum_label.grid(row = 8, column = 0, padx = 10, sticky = "W")

        self.mode_label = tk.Label(self, text = "Mode: Distribution", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        self.mode_label.grid(row = 10, column = 0, padx = 10, sticky = "W")
        self.student_textbooks_label = tk.Label(self, text = "Needed Textbooks: ", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        self.student_textbooks_label.grid(row = 0, column = 1, sticky = "W", pady = (30, 0))
        back_button = controller.make_back_button(controller = self)
        back_button.grid(row = 12, column = 0, padx = 10, pady = (78,0), sticky = "W")
        invisible_label = tk.Label(self, text = "", bg = controller.MAROON)
        invisible_label.grid(row = 13, padx = 150)
        manual_entry = tk.Button(self, text = "Manual Barcode Entry", font = controller.MENU_FONT, command = lambda: window.manual_barcode_entry_window(self, controller).show(controller))
        manual_entry.grid(row = 11, column = 0, padx = 10, sticky = "W")
        self.textbook_listbox = tk.Listbox(self, bd = 0, bg = controller.MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = controller.MAROON, height = 20)
        self.textbook_listbox.grid(row = 1, column = 1, sticky = "NW", rowspan = 20)