import tkinter as tk
from tkinter import messagebox
import window

#where teachers assign textbooks to courses
class TeacherAssignment(tk.Frame):

    idx = -1
    cidx = -1
    current_teacher = ""
    course_selected = False
    teacher_selected = False
    identical_courses = False
    teacher_courses = []
    courses_info = []
    full_courses_info = []
    textbook_nums = 0
    current_textbook_list = []
    changes_made = False
    new_course = False

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass

    def display_teacher_info(self, controller):
        self.course_list.delete(0, tk.END)
        course_check = []
        self.courses_info.clear()
        self.full_courses_info.clear()
        for x, course in enumerate(self.teacher_courses):
            course_info = controller.scanner.server.info_c(course)
            if(self.identical_courses):
                self.course_list.insert(x, course_info[1])
                self.courses_info.append(course_info)
            else:
                if(course_info[1] not in course_check):
                    self.course_list.insert(x, course_info[1])
                    self.courses_info.append(course_info)
                    course_check.append(course_info[1])
            self.full_courses_info.append(course_info)
                    
    def display_identical_courses(self,controller):
        self.identical_courses = not self.identical_courses
        self.display_teacher_info(controller)
        if(self.identical_courses):
            self.identical_button["text"] = "Revert"
        else:
            self.identical_button["text"] = "Display Identical Courses"

    def select_course(self, event, controller):
        if(self.course_list.curselection()):
            check = True
            if(check and self.course_list.curselection()[0] != self.cidx or self.new_course):
                self.new_course = False
                self.changes_made = False
                self.course_selected = True
                self.cidx = (self.course_list.curselection()[0])
                self.course_name_label["text"] = "Course Name: " + self.course_list.get(self.cidx)
                self.course_textbooks.delete(0, tk.END)
                print("COURSE NUMBER: " + str(self.courses_info[self.cidx][0]))
                self.current_course_textbooks = controller.scanner.server.course_r(self.courses_info[self.cidx][0])
                print(self.current_course_textbooks)
                self.textbook_nums = 0
                self.current_textbook_list.clear()
                for textbook in self.current_course_textbooks:
                    if(len(textbook) > 0):
                        self.course_textbooks.insert(self.textbook_nums, textbook)
                        self.textbook_nums += 1
                        self.current_textbook_list.append(textbook)

    def select_textbook(self, event, controller):
        if(self.course_textbooks.curselection()):
            self.idx = (self.course_textbooks.curselection()[0])

    def delete_selected_textbook(self, controller):
        if(self.idx > -1):
            del self.current_textbook_list[self.idx]
            self.course_textbooks.delete(self.idx)
            self.textbook_nums -= 1
            self.changes_made = True
            if(self.identical_courses):
                controller.scanner.server.set_course_r(self.teacher_courses[self.cidx], self.current_textbook_list)
            else:
                for course in self.full_courses_info:
                    if(course[1] == self.courses_info[self.cidx][1]):
                        controller.scanner.server.set_course_r(course[0], self.current_textbook_list)
        else:
            messagebox.showerror("ERROR", "Please select a textbook you would like to delete")

    def add_textbook(self, controller):
        if(not self.teacher_selected):
            messagebox.showerror("Error", "Please let my poor program know who you are before you click fancy buttons -Derek")
        elif(not self.course_selected):
            messagebox.showerror("Error", "Please select a course first before adding textbooks")
        else:
            current_textbook_name = window.add_textbook_window(self, controller).show()
            if(current_textbook_name in self.current_textbook_list):
                messagebox.showwarning("WARNING", "You already have the identical textbook for this course")
            elif(len(current_textbook_name) > 0):
                self.changes_made = True
                self.course_textbooks.insert(self.textbook_nums, current_textbook_name)
                self.current_textbook_list.append(current_textbook_name)
                if(self.identical_courses):
                    controller.scanner.server.set_course_r(self.teacher_courses[self.cidx], self.current_textbook_list)
                else:
                    for course in self.full_courses_info:
                        if(course[1] == self.courses_info[self.cidx][1]):
                            controller.scanner.server.set_course_r(course[0], self.current_textbook_list)

    def confirm_changes(self, controller):
        self.changes_made = False
        self.new_course = True
        print(self.current_textbook_list)
        print(self.cidx)
        if(self.identical_courses):
            controller.scanner.server.set_course_r(self.teacher_courses[self.cidx], self.current_textbook_list)
        else:
            for course in self.full_courses_info:
                if(course[1] == self.courses_info[self.cidx][1]):
                    controller.scanner.server.set_course_r(course[0], self.current_textbook_list)

    #searches for a teacher's name
    def search_teacher(self, controller):
        check = False
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        if(first_name and last_name):
            for t_name in controller.scanner.teachers:
                if(first_name.lower() in t_name.lower() and last_name.lower() in t_name.lower()):
                    if(messagebox.askyesno(title = "Confirm", message = "Are you " + t_name + "?")):
                        check = True
                        self.current_teacher = t_name
                        self.teacher_courses = controller.scanner.server.get_teacher_c(self.current_teacher)
                        print("TEACHER COURSES: ", self.teacher_courses)
                        self.display_teacher_info(controller)
                        self.course_selected = False
                        self.teacher_selected = True
                        break
        if(not check):
            messagebox.showerror(title = "Error", message = "Do you even know how to spell your name?")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TeacherAssignment.configure(self, background = controller.MAROON)

        self.courses = controller.scanner.server.courses_n()
        controller.make_back_button(self).grid(row = 8, column = 0, padx = 10, pady = (40,0))
        self.first_name_entry = tk.Entry(self)
        self.last_name_entry = tk.Entry(self)
        teacher_name_label = tk.Label(self, text = "Who Art Thou?", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        teacher_name_label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2)
        first_name_label = tk.Label(self, text = "First Name:", font = controller.MENU_FONT, bg = controller.MAROON)
        last_name_label = tk.Label(self, text = "Last Name:", font = controller.MENU_FONT, bg = controller.MAROON)
        first_name_label.grid(row = 1, column = 0)
        last_name_label.grid(row = 2, column = 0)
        self.first_name_entry.grid(row = 1, column = 1)
        self.last_name_entry.grid(row = 2, column = 1)

        self.search_button = tk.Button(self, text = "Do I Exist?", font = controller.BUTTON_FONT, command = lambda: self.search_teacher(controller))
        self.search_button.grid(row = 3, column = 0, pady = 10, columnspan = 2)
        courses_label = tk.Label(self, text = "Select Course", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        courses_label.grid(row = 4, column = 0, padx = 10, pady = (5,0), columnspan = 2, sticky = "W")
        self.course_list = tk.Listbox(self, bd = 0, bg = controller.MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = controller.MAROON)
        self.course_list.grid(row = 5, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = "W")
        self.identical_button = tk.Button(self, text = "Display Identical Courses", font = controller.BUTTON_FONT, command = lambda: self.display_identical_courses(controller))
        self.identical_button.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 2, sticky = "W")
        self.course_list.bind('<<ListboxSelect>>', lambda event: self.select_course(event,controller))
        self.invisible_label = tk.Label(self, text = "", bg = controller.MAROON)
        self.invisible_label.grid(row = 0, column = 4, padx = 30)
        self.course_info_label = tk.Label(self, text = "Course Info:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        self.course_info_label.grid(row = 0, column = 5, pady = (10,0), columnspan = 3, sticky = "W")
        self.course_name_label = tk.Label(self, text = "Course Name: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.course_name_label.grid(row = 1, column = 5, sticky = "W", columnspan = 2)
        self.course_section_label = tk.Label(self, text = "Course Section: ", font = controller.MENU_FONT, bg = controller.MAROON)
        self.course_section_label.grid(row = 2, column = 5, sticky = "W")
        self.course_textbook_label = tk.Label(self, text = "Course Textbooks:", font = controller.SUBTITLE_FONT, bg = controller.MAROON)
        self.course_textbook_label.grid(row = 4, column = 5, sticky = "W")
        self.course_textbooks = tk.Listbox(self, bd = 0, bg = controller.MAROON, font = controller.MENU_FONT, selectmode = "SINGLE", selectbackground = controller.MAROON)
        self.course_textbooks.grid(row = 5, column = 5, pady = 5, sticky = "NW")
        self.course_textbooks.bind('<<ListboxSelect>>', lambda event: self.select_textbook(event,controller))
        self.button_container = tk.Frame(self)
        self.button_container["bg"] = controller.MAROON
        self.button_container.grid(row = 5, column = 6, rowspan = 3, pady = 5, sticky = "NW")
        self.remove_textbook_button = tk.Button(self.button_container, text = "Remove Textbook", font = controller.BUTTON_FONT, command = lambda : self.delete_selected_textbook(controller))
        self.remove_textbook_button.grid(row = 1, column = 0, padx = 6, sticky = "N")
        self.add_textbook_button = tk.Button(self.button_container, text = "Add Textbook", font = controller.BUTTON_FONT, command = lambda : self.add_textbook(controller))
        self.add_textbook_button.grid(row = 0, column = 0,  padx = 6, sticky = "W")
        #self.confirm_button = tk.Button(self, text = "Confirm Changes", font = controller.BUTTON_FONT, command = lambda : self.confirm_changes(controller))
        #self.confirm_button.grid(row = 6, column = 5, sticky = "W")