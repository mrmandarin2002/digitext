#Digitext Program written in python as JavaFX is the definition of cancer
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox

from Frames import welcome_page
from Frames import menu
from Frames import textbook_management
from Frames import info
from Frames import textbook_scanner
from Frames import teacher_assignment

import json, traceback
from urllib import request, parse

#import own files
import interactions, barcode_interaction

def slack_message(text):
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

#the center of the universe (digitext really)
class client(tk.Tk):

    #some initialization stuff I found on the internet. Don't know how but it works!
    def __init__(self, *args, **kwargs):
        with open('settings.json') as settings_file:
            self.settings = json.load(settings_file)

        print("IP ADDRESS: " + self.settings["ip_address"])
        print("CLIENT VERSION: " + self.settings["version"])
        tk.Tk.__init__(self, *args, **kwargs)
        
        #this is the list of different windows ("frames as called in tkinter"). The basic idea between page switches...
        #is that I already pre-load all the windows and switch between them as necessary
        self.scene_list = (textbook_management.TextbookManagement,menu.Menu, info.Info, textbook_scanner.TextbookScanner, teacher_assignment.TeacherAssignment)

        self.MAIN_FONT = "Helvetica"
        self.MAROON = "#DFF9FB"
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
        self.show_frame("Menu", False)

    #this shows the frame / window of the page we want to display
    def show_frame(self, page_name, distribution):
        self.frames["TextbookManagement"].day = distribution
        self.current_frame_name = page_name
        self.frames[page_name].clear()
        self.frames[page_name].tkraise()

    #allows the creation of buttons
    def make_button(self, controller, d_text, scene, option, distribution):
        if(option == "menu"):
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene, distribution), font = self.MENU_FONT)
        else:
            return tk.Button(controller, text = d_text, command = lambda: self.show_frame(scene, False), font = self.BUTTON_FONT)
    
    def make_back_button(self, controller):
        return tk.Button(controller, text = "Back to Menu", command = lambda: self.show_frame("Menu", False), font = self.BACK_BUTTON_FONT)

if __name__ == '__main__':
    root = client()
    root.title("DigiText")
    root.geometry("600x500")
    root.resizable(False, False)
    root.mainloop()

            



