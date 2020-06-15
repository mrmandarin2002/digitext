#Digitext Program written in python as JavaFX is the definition of cancer
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox

from Frames import *

#import own files
import interactions, barcode_interaction

#the center of the universe (digitext really)
class client(tk.Tk):

    #there will likely be a few versions of this program (students will have a restricted version)
    version = "teacher"

    #some initialization stuff I found on the internet. Don't know how but it works!
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #this is the list of different windows ("frames as called in tkinter"). The basic idea between page switches...
        #is that I already pre-load all the windows and switch between them as necessary
        self.scene_list = (welcome_page.WelcomePage, menu.Menu, textbook_management.TextbookManagement, info.Info, textbook_scanner.TextbookScanner, teacher_assignment.TeacherAssignment)

        self.MAIN_FONT = "Helvetica"
        self.MAROON = '#FFE8F6'
        self.PINK = '#FF00D4'

        #different type of fonts used throughout the program
        self.TITLE_FONT = tkfont.Font(family=self.MAIN_FONT, size=22, weight="bold")
        self.SUBTITLE_FONT = tkfont.Font(family = self.MAIN_FONT, size = 15, weight = "bold")
        self.FIELD_FONT = tkfont.Font(family = self.MAIN_FONT, size = 11)
        self.BUTTON_FONT = tkfont.Font(family= self.MAIN_FONT, size=10)
        self.BACK_BUTTON_FONT = tkfont.Font(family = self.MAIN_FONT, size = 8)
        self.MENU_FONT = tkfont.Font(family= self.MAIN_FONT, size=13)

        #self.scanner allows for barcode input and server communication
        #the relevant code is in barcode_interactions.py
        self.scanner = barcode_interaction.scanner(self)

        print("CURRENT TEXTBOOK LIST:")
        print(self.scanner.textbook_list)

        #some other lines of code that the stack overflow provided
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        #where I keep all my windows and switch between them
        self.frames = {}

        #initializes all the windows / pages
        for scene in self.scene_list:
            page_name = scene.__name__
            frame = scene(parent=container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nswe")

        #this is the starting window
        self.show_frame("WelcomePage")

    #this shows the frame / window of the page we want to display
    def show_frame(self, page_name):
        self.current_frame_name = page_name
        self.frames[page_name].clear()
        self.frames[page_name].tkraise()

    #allows the creation of buttons
    def make_button(self, controller, d_text, scene, option):
        if(option == "menu"):
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.MENU_FONT, fg = self.PINK)
        else:
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene), font = self.BUTTON_FONT)
    
    def make_back_button(self, controller):
        return tk.Button(controller, text = "Back to Menu", command = lambda: self.show_frame("Menu"), font = self.BACK_BUTTON_FONT)

root = client()
root.title("DigiText")
root.iconbitmap("sphs_icon.ico")
root.geometry("600x500")
root.resizable(False, False)
root.mainloop()

        



