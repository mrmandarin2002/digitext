import tkinter as tk
import threading

#welcome screen, no need to explain
class Stats(tk.Frame):

    in_thread = False

    def clear(self):
        pass

    def barcode_scanned(self, controller):
        pass

    def can_enter(self, controller):
        controller.check_requisites = True

    def check_number(self):
        threading.Timer(1, self.check_number).start()
        if(self.controller.current_frame_name == "Stats" and not self.in_thread):
            num_data = self.controller.scanner.get_textbook_nums()
            self.in_thread = True
            self.welcome_title["text"] = "Number Of Textbooks: " + str(num_data[0])
            self.assigned_textbooks["text"] = "Textbooks To Go: " + str(num_data[1])
            self.distributed_textbooks["text"] = "Textbooks Distributed: " + str(num_data[2])
            self.students_left["text"] = "Students To Go: " + str(num_data[3])
            self.student_listbox.delete(0, tk.END)
            print(num_data)
            for x in range(4, len(num_data)):
                self.student_listbox.insert(x, str(num_data[x]))
            self.in_thread = False
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Stats.configure(self, background = controller.MAROON)
        self.welcome_title = tk.Label(self, text = "Number Of Textbooks: ", font = controller.TITLE_FONT2 , bg = controller.MAROON)
        self.welcome_title.pack(side = "top", pady = 4, padx = 0)
        self.assigned_textbooks = tk.Label(self, text = "Textbooks To Go: ", font = controller.TITLE_FONT2, bg = controller.MAROON)
        self.assigned_textbooks.pack(side = "top", pady = 4, padx = 0)
        self.distributed_textbooks = tk.Label(self, text = "Textbooks Distributed: ", font = controller.TITLE_FONT2, bg = controller.MAROON)
        self.distributed_textbooks.pack(side = "top", pady = 4, padx = 0)
        self.students_left = tk.Label(self, text = "Students To Go: ", font = controller.TITLE_FONT2, bg = controller.MAROON)
        self.students_left.pack(side = "top", pady = 2, padx = 0)
        self.scanning_label = tk.Label(self, text = "Students Currently Scanning: ", font = controller.ENTRY_FONT, bg = controller.MAROON)
        self.scanning_label.pack(side = "top", pady = 4, padx = 0)
        self.student_listbox = tk.Listbox(self, bd = 0, bg = controller.MAROON, font = controller.ENTRY_FONT, selectmode = "SINGLE", selectbackground = controller.MAROON, height = 16, width = 40)
        self.student_listbox.pack(side = "top", pady = 4, padx = 0)
        export_textbook_info_button = tk.Button(self, text = "Export Textbook Info", font = controller.MENU_FONT, command = controller.scanner.server.get_textbook_inventory)
        export_textbook_info_button.pack(pady = (10, 0))
        controller.make_back_button(self).pack(pady = (10, 0))
        self.check_number()