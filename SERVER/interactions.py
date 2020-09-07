# import neccessary classes and functions
from datetime import datetime
import Database
import string
import time

textbook_dictionary = {}
student_dictionary = {}

def fill_dictionaries():
    start_time = time.time()
    conn = Database.create_connection("server.db")
    textbooks = Database.get_textbooks(conn)
    students = Database.get_students(conn)
    cnt = 0
    for textbook in textbooks:
        try:
            textbook_dictionary[int(textbook[1])] = textbook
            if(int(textbook[1]) < 1000000 or int(textbook[1]) >= 10000000):
                cnt += 1
                #print("Bad Textbook #" + str(cnt) + "!", textbook)
        except:
            print("Error, could not process:", textbook)
    for student in students:
        if(student[4] != ''):
            #print(student)
            student_dictionary[int(student[1])] = student
    print("Fill Dicionary Processing Time: %s seconds ---" % (time.time() - start_time))


# function to get the current time
def get_time():
    return str(datetime.now()).split()[1].split(".")[0]+" "

# checks if a student is valid in the database
def valid_student(args): # student number
    #args[0] = "".join([i for i in args[0].lower() if i not in string.ascii_lowercase])
    print(get_time()+"Checking if "+args[0]+" is a valid student id...")
    try:
        if(int(args[0]) in student_dictionary):
            print(get_time() + "Student ID is valid")
            return '1'
        else:
            print(get_time() + "Student ID is invalid")
            return '0'
    except:
        print("Used Heinrich's Code for valid_student :(") 
        conn = Database.create_connection("server.db")
        students = Database.get_students(conn)
        for student in students:
            if student[1] == str(args[0]):
                conn.close()
                print(get_time() + "Student ID is valid")
                return "1"
        conn.close()
        print(get_time() + "Student ID is invalid")
        return "0" 

# adds a student to the database
def add_student(args):
    conn = Database.create_connection("server.db")
    Database.insert_student(conn, args[0], args[1], args[2])
    conn.close()
    return "1"

# gets student information from the database
def information_student(args): # student number
    #args[0] = "".join([i for i in args[0].lower() if i not in string.ascii_lowercase]
    start_time = time.time()
    print(get_time()+"Returning information of student "+args[0]+"...")
    try:
        student_info = student_dictionary[int(args[0])]
        student_strings = []
        for i in student_info:
            student_strings.append(str(i))
        return "|".join(student_strings)
    except:
        print("Used Heinrich's Code for valid_textbook :(") 
        conn = Database.create_connection("server.db")
        students = Database.get_students(conn)
        for student in students:
            if student[1] == str(args[0]):
                student_strings = []
                for i in student:
                    student_strings.append(str(i))
                conn.close()
                print("Information Student: %s seconds ---" % (time.time() - start_time))
                return "|".join(student_strings)

# get textbooks assigned to a student
def student_textbooks(args): # student number
    #args[0] = "".join([i for i in args[0].lower() if i not in string.ascii_lowercase])
    print(get_time()+"Returning textbooks currently held by student: "+args[0])
    conn = Database.create_connection("server.db")
    textbooks = []
    for t in Database.get_textbooks(conn):
        if t[5] == args[0]:
            textbooks.append(t[1])
    return "|".join(textbooks)

# gets the textbook return information of a specific student from the database
# the information consists of a list: entries from the returned textbooks table corresponding to the student
def student_return_info(args): # student number
    #args[0] = "".join([i for i in args[0].lower() if i not in string.ascii_lowercase])
    print(get_time()+"Returning textbook return information of student "+args[0]+"...")
    conn = Database.create_connection("server.db")
    # get the textbooks returned by the student
    student_returned_textbooks = []
    for textbook in Database.get_returned_textbooks(conn):
        if textbook[2] == args[0]:
            student_returned_textbooks.append("|".join([str(field) for field in textbook]))
    # return gathered information
    return "~".join(student_returned_textbooks)

# get textbooks that a student should have
def student_requisites(args): # student number
    #args[0] = "".join([i for i in args[0].lower() if i not in string.ascii_lowercase])
    print(get_time()+"Returning requisite textbooks for student: "+args[0])
    conn = Database.create_connection("server.db")
    for s in Database.get_students(conn):
        if s[1] == args[0]:
            courses = s[4].split("|")
    textbooks = []
    for c in Database.get_courses(conn):
        if c[1] in courses:
            textbooks.append(c[4].split("|"))
    return "|".join(textbooks)

# get the textbooks that a student has withdrawn
def student_withdrawn(args):
    start_time = time.time()
    print(get_time()+"Returning textbooks withdrawn by student: "+args[0]+"...")
    textbook_ids = (student_textbooks(args)).split('|')
    textbooks_titles = []
    for textbook_id in textbook_ids:
        textbook_info = information_textbook([textbook_id])
        textbook_info = textbook_info.split("|")
        textbooks_titles.append(textbook_info[1])
    print("Student Withdrawn: %s seconds ---" % (time.time() - start_time))
    return "|".join(textbooks_titles)

# get pairs of all student numbers and names
def get_student_pairs(args):
    print(get_time()+"Returning student name-id pairs...")
    conn = Database.create_connection("server.db")
    a = "~".join([i[1]+"|"+i[2] for i in Database.get_students(conn)])
    conn.close()
    return a

# checks if a textbook is valid in the database
def valid_textbook(args): # textbook number
    print(get_time()+"Checking if "+args[0]+" is a valid textbook id...")
    try:
        if(int(args[0]) in textbook_dictionary):
            return '1'
        else:
            return '0'
    except:
        print("Used Heinrich's Code for valid_textbook :(") 
        conn = Database.create_connection("server.db")
        textbooks = Database.get_textbooks(conn)
        for textbook in textbooks:
            if textbook[1] == str(args[0]):
                conn.close()
                print(get_time() + "Textbook ID is valid")
                return "1"
        conn.close()
        print(get_time() + "Textbook ID is invalid")
        return "0"

# gets textbook information from the database
def information_textbook(args): # textbook number
    start_time = time.time()
    print(get_time()+"Returning information of textbook "+args[0]+"...")
    try:
        #more efficient way
        textbook_info = textbook_dictionary[int(args[0])]
        textbook_strings = []
        for i in textbook_info:
            textbook_strings.append(str(i))
        #print("Information textbook: %s seconds ---" % (time.time() - start_time))
        #print(textbook_strings)
        return '|'.join(textbook_strings[1:])
    except:
        #heinrich's way
        print("Had to use Heinrich's method for info_textbook :(")
        conn = Database.create_connection("server.db")
        textbooks = Database.get_textbooks(conn)
        for textbook in textbooks:
            if textbook[1] == str(args[0]):
                textbook_strings = []
                for i in textbook:
                    textbook_strings.append(str(i))
                # textbook_strings[-1] = str(Database.get_studentNumber(conn, textbook_strings[-1]))
                conn.close()
                print("Information textbook: %s seconds ---" % (time.time() - start_time))
                return "|".join(textbook_strings[1:])

# delete textbook from database
def delete_textbook(args): # textbook number
    print(get_time()+"Deleting "+args[0]+" from textbook table...")
    conn = Database.create_connection("server.db")
    Database.remove_textbook(conn, args[0])
    try:
        del textbook_dictionary[int(args[0])]
    except:
        print("Guess you don't exist :/")
    conn.close()
    return "1"

# add a textbook to the database
def add_textbook(args): # textbook number, title, cost, condition
    print(get_time()+"Adding textbook to database\n\tNumber: "+args[0]+"\n\tTitle: "+args[1]+"\n\tCost: "+args[2]+"\n\tCondition: "+args[3])
    conn = Database.create_connection("server.db")
    textbook_dictionary[int(args[0])] = [-1, args[0], args[1], args[2], args[3], None]
    Database.insert_textbook(conn, args[0], args[1], args[2], args[3])
    conn.close()
    return "1"

# assign a textbook to a student in the database
def assign_textbook(args): # textbook number, student number
    print(get_time()+"Assigning textbook: "+args[0]+" to student: "+args[1]+" in database...")
    conn = Database.create_connection("server.db")
    textbook_info = textbook_dictionary[int(args[0])]
    textbook_strings = []
    for i in textbook_info:
        textbook_strings.append(i)
    textbook_strings[5] = args[1]
    textbook_dictionary[int(args[0])] = tuple(textbook_strings)
    Database.assign_textbook(conn, args[0], args[1])
    conn.close()
    return "1"

# return a textbook from a student in the database
def return_textbook(args):
    print(get_time()+"Returning textbook: "+args[0]+" with condition: "+args[1]+" from student...")
    conn = Database.create_connection("server.db")
    Database.return_textbook(conn, args[0], args[1])
    Database.update_condition(conn, args[0], args[1])
    Database.assign_textbook(conn, args[0], "None")
    textbook_info = textbook_dictionary[int(args[0])]
    textbook_strings = []
    for i in textbook_info:
        textbook_strings.append(i)
    textbook_strings[5] = None
    textbook_strings[4] = args[1]
    textbook_dictionary[int(args[0])] =tuple(textbook_strings)
    conn.close()
    return "1"

# return the requisite textbooks for a given course
def course_requisites(args):
    print(get_time()+"Getting course requisites for course: "+args[0])
    conn = Database.create_connection("server.db")
    for c in Database.get_courses(conn):
        if c[1] == args[0]:
            return c[4]

# return information for a specified course
def information_course(args):
    print(get_time()+"Returning information for course: "+args[0])
    conn = Database.create_connection("server.db")
    for c in Database.get_courses(conn):
        if c[1] == args[0]:
            course = list(c[1:])
    for i in range(len(course)):
        course[i] = str(course[i])
    conn.close()
    return "~".join(course)

# return all course numbers from database
def course_numbers(args):
    print(get_time()+"Returning all course numbers...")
    conn = Database.create_connection("server.db")
    numbers = []
    for c in Database.get_courses(conn):
        numbers.append(c[1])
    conn.close()
    return "|".join(numbers)

# sets the requisite textbooks for a given course
def set_course_textbooks(args):
    print(get_time()+"Setting textbooks:\n\t"+"\n\t".join(args[1].split("~"))+"\nAs requisites to course: "+args[0])
    conn = Database.create_connection("server.db")
    Database.set_course_requisites(conn, args[0], args[1].replace("~", "|"))
    conn.close()
    return "1"

# gets information of all teachers
def get_teachers(args):
    print(get_time()+"Getting teacher names and numbers...")
    conn = Database.create_connection("server.db")
    teachers = []
    for course in Database.get_courses(conn):
        if course[3] not in teachers:
            teachers.append(course[3])
    conn.close()
    return "|".join(teachers)

# gets the course numbers for a specified teacher
def get_teacher_courses(args):
    print(get_time()+"Getting courses of teacher: "+args[0]+"...")
    conn = Database.create_connection("server.db")
    courses = []
    for course in Database.get_courses(conn):
        if course[3] == args[0] and course[1] not in courses:
            courses.append(course[1])
    conn.close()
    return "|".join(courses)

# gets a list of textbook names
def get_textbook_names(args):
    print(get_time()+"Getting a list of textbook names...")
    conn = Database.create_connection("server.db")
    textbooks = []
    for textbook in Database.get_textbooks(conn):
        if textbook[2] not in textbooks:
            textbooks.append(textbook[2])
    for i in range(len(textbooks)):
        textbooks[i] = str(textbooks[i])
    return "|".join(textbooks)

# gets a list of textbook counts
def get_textbook_counts(args):
    print(get_time()+"Getting textbook counts...")
    conn = Database.create_connection("server.db")
    textbooks = {}
    for textbook in Database.get_textbooks(conn):
        if textbook[2] in textbooks.keys():
            textbooks[textbook[2]] += 1
        else:
            textbooks[textbook[2]] = 1
    serialized = []
    for k in textbooks.keys():
        serialized.append(k+"|"+str(textbooks[k]))
    conn.close()
    return "~".join(serialized)

# gets the total number of textbooks
def get_textbook_total(args):
    print(get_time()+"Getting total number of textbooks...")
    conn = Database.create_connection("server.db")
    total = len(Database.get_textbooks(conn))
    conn.close()
    return total

# gets textbook inventory
def get_textbook_inventory(args):
    print(get_time()+"Getting textbook inventory...")
    conn = Database.create_connection("server.db")
    textbooks = {}
    for textbook in Database.get_textbooks(conn):
        if textbook[2] not in textbooks.keys():
            conditions = [0]*5
            conditions[textbook[4]] += 1
            textbooks[textbook[2]] = [textbook[3]]+conditions+[1]
        else:
            if textbook[3] > textbooks[textbook[2]][0]:
                textbooks[textbook[2]][0] = textbook[3]
            textbooks[textbook[2]][textbook[4]+1] += 1
            textbooks[textbook[2]][-1] += 1
    keys = list(textbooks.keys())
    keys.sort()
    output = []
    for k in keys:
        output.append(k+"|"+"|".join([str(i) for i in textbooks[k]]))
    conn.close()
    return "~".join(output)

# merges textbooks
def merge_database_textbooks(args):
    conn = Database.create_connection("server.db")
    sql_cmd = """UPDATE Textbooks
                 SET TextbookTitle = ?
                 WHERE TextbookTitle = ?"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (args[1], args[0]))
    conn.commit()
    return "1"

# ping (always return 1)
def ping(args): # no arguments
    # print(get_time()+"Received ping...")
    return "1"

# interactions function dictionary
interact = {"valid_t": valid_textbook,
            "valid_s": valid_student,
            "info_t": information_textbook,
            "info_s": information_student,
            "info_c": information_course,
            "delete_t": delete_textbook,
            "student_t": student_textbooks,
            "student_r": student_requisites,
            "student_returned": student_return_info,
            "student_withdrawn": student_withdrawn,
            "student_pairs": get_student_pairs,
            "get_teachers": get_teachers,
            "get_teacher_c": get_teacher_courses,
            "set_course_r": set_course_textbooks,
            "get_textbook_titles": get_textbook_names,
            "get_textbook_counts": get_textbook_counts,
            "get_textbook_inv": get_textbook_inventory,
            "get_textbook_total": get_textbook_total,
            "add_t": add_textbook,
            "merge_t": merge_database_textbooks,
            "add_s": add_student,
            "courses_n": course_numbers,
            "course_r": course_requisites,
            "assign_t": assign_textbook,
            "return_t": return_textbook,
            "p": ping}
