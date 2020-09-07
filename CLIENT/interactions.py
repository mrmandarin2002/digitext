import socket, threading
from tkinter import messagebox

import window

HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class Client:

    server_connection = True
    displayed_error = False

    def find_connection(self):
        # initialize socket
        self.connection_established = False
        while(not self.connection_established):
            try:
                # define server address
                self.server_address = (self.address, self.port)
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect(self.server_address)
                self.tcp_socket.settimeout(5)
                self.connection_established = True
            except:
                messagebox.showerror("Connection Error!", "Please enter the IP Address of the server. Merci.")
                window.ip_config_window(self.controller).show(self.controller)
                self.address = self.controller.ip_address
                self.controller.update_settings()


    # initialization method
    def __init__(self, controller, address, port, debug_mode=False):
        self.controller = controller
        self.address = address
        self.port = port
        self.find_connection()

    # basic data echo method
    def echo(self, msg):
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        success = False
        try:
            self.tcp_socket.send(send_length)
            success = True
        except:
            self.connection_established = False
            self.find_connection()
        if(success):
            self.tcp_socket.send(msg.encode("utf-8"))
            data_length = ""
            cnt = 0
            while (len(data_length) < HEADER):
                cnt += 1
                data_length += self.tcp_socket.recv(HEADER).decode(FORMAT)
            if(int(data_length)):
                data = ""
                cnt = 0
                while(len(data) < int(data_length)):
                    data += (self.tcp_socket.recv(int(data_length))).decode("utf-8")
                    cnt += 1
                return data # return decoded data
            else:
                return ""
        else:
            return ""

    # command method
    def command(self, cmd, args):
        # only loop through the arguments array if there is at least one argument
        if len(args) > 0:
            # create initial message string, including the first element of the arguments list
            msg = cmd+";"+args[0]
            # add remaining elements of the arguments array
            if len(args) > 1:
                for arg in args[1:]:
                    msg += "|"+arg
            # return the response of the fully formed message string
            return self.echo(msg)
        else:
            return self.echo(cmd+";")

    # ping method (returns true if the server responds in less than one second)
    def ping(self):
        if self.command("p", []) == "1":
            return True
        else:
            return False

    # student id validation method
    def valid_s(self, student_id):
        if self.command("valid_s", [student_id]) == "1":
            return True
        else:
            return False

    # get student information
    def info_s(self, student_id):
        return self.command("info_s", [student_id]).split("|")

    # delete a textbook from the database
    def delete_t(self, textbook_id):
        return self.command("delete_t", [textbook_id])

    # add a textbook to the database
    def add_t(self, textbook_id, textbook_name, textbook_price, textbook_condition):
        return self.command("add_t", [textbook_id, textbook_name, textbook_price, textbook_condition])

    # add a student to the database
    def add_s(self, student_id, student_name, student_deposit):
        return self.command("add_s", [student_id, student_name, student_deposit])

    # get student textbooks from the database
    def student_t(self, student_id):
        value = self.command("student_t", [student_id]).split("|")
        if value[0] == "":
            return []
        else:
            return value

    # get student withdrawn textbooks
    def student_withdrawn(self, student_id):
        return self.command("student_withdrawn", [student_id]).split("|")

    # get student pairs
    def student_pairs(self):
        return [i.split("|") for i in self.command("student_pairs", []).split("~")]

    # textbook id validation method
    def valid_t(self, textbook_id):
        if self.command("valid_t", [textbook_id]) == "1":
            return True
        else:
            return False

    # get textbook information from the database
    def info_t(self, textbook_id):
        return self.command("info_t", [textbook_id]).split("|")

    # assign textbook to student in database
    def assign_t(self, textbook_id, student_id):
        return self.command("assign_t", [textbook_id, student_id])

    # retun textbook from student in database
    def return_t(self, textbook_id, textbook_condition):
        return self.command("return_t", [textbook_id, str(textbook_condition)])

    # get a list of all course numbers
    def courses_n(self):
        return self.command("courses_n", []).split("|")

    # get a list of requisite textbooks for a given course
    def course_r(self, course_id):
        return self.command("course_r", [course_id]).split("|")

    # get course information for a given course
    def info_c(self, course_id):
        return self.command("info_c", [course_id]).split("~")
    
    # sets the requisite textbooks for a course
    def set_course_r(self, course_id, course_r):
        return self.command("set_course_r", [course_id, "~".join(course_r)])

    # gets a list of teacher names
    def get_teachers(self):
        return self.command("get_teachers", []).split("|")
    
    # gets the list of courses for a given teacher
    def get_teacher_c(self, teacher_name):
        return self.command("get_teacher_c", [teacher_name]).split("|")
    
    # gets a list of textbook titles
    def get_textbook_titles(self):
        return self.command("get_textbook_titles", []).split("|")
    
    # get a list of textbook counts:
    def get_textbook_counts(self):
        #test_data = self.command("get_textbook_counts", [])
        #print("Test Data: " + str(test_data))
        data = [i.split("|") for i in self.command("get_textbook_counts", []).split("~")]
        #print("Interaction Test: " + str(data))
        return data

    # get the total number of textbooks
    def get_textbook_total(self):
        return int(self.command("get_textbook_total", []))

    # write textbook inventory to file
    def get_textbook_inventory(self):
        open("textbook_inventory.csv", "w").write("title,price,new,good,fair,poor,destroyed,total\n"+self.command("get_textbook_inv", []).replace("|", ",").replace("~", "\n"))

    # get a list of returned textbooks for a specified student
    def get_student_returned(self, student_id):
        return [textbook.split("|") for textbook in self.command("student_returned", [student_id]).split("~")]

    # merge two textbooks in the database
    def merge_textbooks(self, original, new):
        return self.command("merge_t", [original, new])

    def student_r(self, student_id):
        return self.command("student_r", [student_id]).split('|')
        

