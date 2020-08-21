import tkinter as tk

#menu, basically a window where you can go into the more important frames   
class Menu(tk.Frame):

    def clear(self):
        pass
    
    def barcode_scanned(self, controller):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Menu.configure(self, background = controller.MAROON)
        menu_title = tk.Label(self, text = "DigiText Menu", font = controller.TITLE_FONT , bg = controller.MAROON)
        d_button = controller.make_button(controller = self, d_text = "Textbook Distribution", scene = "TextbookManagement", option = "menu", distribution = 'D')
        r_button = controller.make_button(controller = self, d_text = "Textbook Return", scene = "TextbookManagement", option = "menu", distribution = 'R')
        stats_button = controller.make_button(controller = self, d_text = "Stats", scene = "Stats", option = "menu", distribution = 'N')
        menu_title.pack(pady = (100, 0))
        d_button.pack(pady = (50, 0))
        r_button.pack()
        if(controller.settings["version"] == "teacher"):
            s_button = controller.make_button(controller = self, d_text = "Add Textbooks", scene = "TextbookScanner", option = "menu", distribution = 'N')
            i_button = controller.make_button(controller = self, d_text = "Student/Textbook Lookup", scene = "Info", option = "menu", distribution = 'N')
            t_button = controller.make_button(controller = self, d_text = "Teacher/Course Textbook Assignments", scene = "TeacherAssignment", option = "menu", distribution = 'N')
            s_button.pack()
            i_button.pack()
            t_button.pack()
        stats_button.pack()