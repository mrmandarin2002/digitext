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
        m_button = controller.make_button(controller = self, d_text = "Textbook Distribution & Return", scene = "TextbookManagement", option = "menu")
        s_button = controller.make_button(controller = self, d_text = "Add Textbooks", scene = "TextbookScanner", option = "menu")
        i_button = controller.make_button(controller = self, d_text = "Student/Textbook Lookup", scene = "Info", option = "menu")
        t_button = controller.make_button(controller = self, d_text = "Teacher/Course Textbook Assignments", scene = "TeacherAssignment", option = "menu")
        menu_title.pack(pady = (100, 0))
        m_button.pack(pady = (50, 0))
        s_button.pack()
        i_button.pack()
        t_button.pack()