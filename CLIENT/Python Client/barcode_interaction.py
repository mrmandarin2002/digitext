import time
#own files
import interactions
#allow to keep track of time
from datetime import datetime
#pynput's library for enabling threading
from pynput.keyboard import Key, Listener
from tkinter import messagebox

#####
#the scanner class is how the program detects input from the barcode
#also where data regarding the specifics of the scanned barcode is procssed
#basic idea for barcode detection is that since the barcode scanner sends input as keyboard...
#we can basically have a temporary string that keeps track of keyboard inputs. This string clears...
#every time more than 40 milliseconds elapses between inputs
#also keeps a lot of data regarding textbooks
#####

class scanner:

    #a temporary string to keep track of characters being added
    barcode_string = ""
    #identification of the type of the barcode
    barcode_status = ""
    #keeps track of the current time
    start = datetime.now()
    #keeps track of the time of the last input
    previous_time = 0
    #the textbooks currently taken out by a student
    student_textbooks = []
    #student's info {
    #1 : barcode 
    #2 : name
    #3 : ?
    #4 : textbooks
    #5 - ? : courses
    # }
    student_info = []
    #list of textbooks assigned by teachers
    student_needed_textbooks = []
    #courses that a student takes
    student_courses = []
    #the titles of the student's textbooks (student_textbooks is based on barcode id)
    student_textbooks_title = []
    #a textbook's info{
    #0 : barcode
    #1 : title
    #2 : price
    #3 : condition
    # }
    textbook_info = []
    #list of all textbooks
    textbook_list = []
    
    textbook_conditions = ["New", "Good", "Fair", "Poor", "Destroyed"]
    textbook_conditions_rev = {"New": 0, "Good": 1, "Fair": 2, "Poor": 3, "Destroyed": 4}

    def get_textbook_nums(self):
        self.textbook_nums = self.server.get_textbook_counts()
        self.total_textbooks = 0
        if(len(self.textbook_nums) > 3):
            for textbook in self.textbook_nums:
                self.total_textbooks += int(textbook[1])
            print("Total Amount Of Textbooks " + str(self.total_textbooks))
        return self.total_textbooks

    def __init__(self, controller):
        self.controller = controller
        #where the interaction with server happens
        self.server = interactions.Client(address = controller.settings["ip_address"], port = 7356)
        #all the courses available
        self.courses = self.server.courses_n()
        #all the teachers at the school
        self.teachers = self.server.get_teachers()
        #all the textboosk at school
        self.textbook_list = self.server.get_textbook_titles()
        #sort the textbook_list alphabetically
        self.textbook_list = sorted(self.textbook_list)
        self.textbook_nums = self.server.get_textbook_counts()
        print("Textbook Count:")
        print(self.textbook_nums)
        self.total_textbooks = 0
        if(len(self.textbook_nums) > 3):
            for textbook in self.textbook_nums:
                self.total_textbooks += int(textbook[1])
            print("Total Amount of textbooks:" + str(self.total_textbooks))

        #starts the thread where program listens for input (if there is input call on_press function below)
        keyLis = Listener(on_press=lambda key : self.on_press(key, controller))
        keyLis.start()
        
    #function that is called whenever there is input from a device
    #note that time is in microseconds
    def on_press(self, key, controller):
        #the amount of time between current input and previous input (converted into micro seconds)
        time_elapsed = (datetime.now() - self.start).microseconds + (datetime.now() - self.start).seconds * 1000000
        #this assumes that the input is from barcode scanner as the time between inputs is less than 40 milliseconds
        if(time_elapsed - self.previous_time < 50000):
            #add input to the temporary string (self.barcode_string)
            #we don't want the enter or shift key to be added as to our final string
            if(key != Key.enter and key != Key.shift):
                self.barcode_string += str(key)[1:-1]
            #since the final input of scanner is always enter, if the string we have been adding to is a certain length...
            #the program decides its a barcode. It's quite foolproof
            if(key == Key.enter and len(self.barcode_string) > 5):
                print("IN")
                #this makes "self.current_barcode" our official barcode id! For now...
                self.current_barcode = self.barcode_string
                #reset the the temporary barcode string
                self.barcode_string = ""
                self.current_barcode = ''.join(i for i in self.current_barcode if i.isdigit())
                #checks what the actual hell the barcode is
                self.check_barcode(controller)
        else:
            #in case this is the start of a scanner's input, we add the first ccharacter
            self.barcode_string = str(key)[1:-1]
            #once again it would be bad if shifts or enters somehow entered our temporary string...
            if(key == Key.shift or key == Key.enter):
                self.barcode_string = ""
        #sets the time of this 
        self.previous_time = time_elapsed  

    #this function checks what the hell the barcode is
    def check_barcode(self, controller):
        error = False
        print("Barcode: " + self.current_barcode)
        #check's if it's a textbook's barcode
        if(self.server.valid_t(self.current_barcode)):
            print("TEXTBOOK BARCODE!")
            self.textbook_info = self.server.info_t(self.current_barcode)
            if(len(self.textbook_info) > 2):
                self.barcode_status = "Textbook"
            else:
                error = True
        #checks if the barcode is a student's
        elif(self.server.valid_s(self.current_barcode)):
            #gets the student's info from the server
            self.student_info = self.server.info_s(self.current_barcode)
            #for debugging I guess
            print("STUDENT BARCODE!")
            print("Student Info: ")
            print(self.student_info)
            if(len(self.student_info) > 2):
                #gets the textbooks the student has taken out
                self.student_textbooks = self.server.student_t(self.current_barcode)
                #clears a bunch of lists so that the relevant stuff can be added
                self.student_needed_textbooks.clear()
                self.student_textbooks_title.clear()
                self.student_courses.clear()
                #this creates a list of student's textbooks based on title instead of barcode ID
                #useful for comparisons....
                for textbook in self.student_textbooks:
                    self.student_textbooks_title.append(self.server.info_t(textbook)[1])
                #this creates a list of a student's courses with the help of student_info
                for x in range(4, len(self.student_info)):
                    #gets info of a student's courses
                    course_info = self.server.info_c(self.student_info[x])
                    #adds course to a student's course
                    self.student_courses.append(course_info)
                    #the textbooks needed in this course
                    course_textbooks = course_info[3].split('|')
                    #this loop is to find out which textbooks the student needs to take out that were assigned to him
                    for textbook in course_textbooks:
                        #checks for duplicates and idek 
                        if(len(textbook) > 0 and textbook not in self.student_needed_textbooks and textbook not in self.student_textbooks_title):
                            self.student_needed_textbooks.append(textbook)
                #allows other parts of the program know what type of barcode is scanned in
                self.barcode_status = "Student"
            else:
                error = True
        else:
            print("UNKNOWN BARCODE!")
            self.barcode_status = "Unknown"   
        if(not error):
            controller.frames[controller.current_frame_name].barcode_scanned(controller = self) 
        else:
            messagebox.showerror("ERROR", "Don't Touch This Piece Of Garbage And Find Senpai Derek ASAP.")
    
    #updates the textbook_list to include the latest books
    def update_textbook_list(self):
        self.textbook_list = self.server.get_textbook_titles()
