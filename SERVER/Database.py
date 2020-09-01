import sqlite3
from sqlite3 import Error
import os, shutil, xlrd

def reset_database(db_file, db_backup):
    os.remove(db_file)
    shutil.copy(db_backup, db_file)

def create_connection(db_file):
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    conn.close()

def insert_student(conn, number, name, deposit):
    # create an sql command string
    sql_cmd = """INSERT INTO Students(StudentNumber, StudentName, StudentDeposit, StudentCourses)
             VALUES(?,?,?, ?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (str(number), str(name), float(deposit), ""))
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted sutdent
    return cur.lastrowid

def remove_student(conn, StudentNumber):
    # create an sql command string using the function parameter
    sql_cmd = "DELETE FROM Students WHERE StudentNumber=\""+str(StudentNumber)+"\";"
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string
    cur.execute(sql_cmd)
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()

def get_students(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("SELECT * FROM Students WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

def get_studentNumber(conn, studentId):
    students = get_students(conn)
    for student in students:
        if student[0] == studentId:
            return str(student[1])

def insert_textbook(conn, number, title, cost, condition):
    # create an sql command string
    sql_cmd = """INSERT INTO Textbooks(TextbookNumber, TextbookTitle, TextbookCost, TextbookCondition)
                 VALUES (?,?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (number, title, cost, condition))
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted textbook
    TextbookId = cur.lastrowid
    cur.close()
    return TextbookId

def remove_textbook(conn, TextbookNumber):
    # create an sql command string using the function parameter
    sql_cmd = "DELETE FROM Textbooks WHERE TextbookNumber=\""+str(TextbookNumber)+"\";"
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string
    cur.execute(sql_cmd)
    cur.close() # close the cursor object
    # commit the changes to the database
    conn.commit()

def get_textbooks(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("select * FROM Textbooks WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

def assign_textbook(conn, TextbookNumber, StudentNumber):
    # get textbook information
    for t in get_textbooks(conn):
        if t[1] == TextbookNumber:
            textbook = list(t)
    if textbook:
        textbook[5] = StudentNumber
        textbook.append(textbook[0])
        textbook = textbook[1:]
        # create a cursor object
        cur = conn.cursor()
        # create an sql command string to update textbooks table with new information
        sql = """UPDATE Textbooks
                SET TextbookNumber = ? ,
                    TextbookTitle = ? ,
                    TextbookCost = ? ,
                    TextbookCondition = ? ,
                    StudentNumber = ?
                WHERE TextbookId = ?"""
        # execute sql command string with selected textbook as input parameters and close cursor object
        cur.execute(sql, textbook)
        cur.close()
        # commit the changed database
        conn.commit()

def update_condition(conn, TextbookNumber, Condition):
    # get textbook information
    for t in get_textbooks(conn):
        if t[1] == TextbookNumber:
            textbook = list(t)
    if textbook:
        textbook[4] = Condition
        textbook.append(textbook[0])
        textbook = textbook[1:]
        # create a cursor object
        cur = conn.cursor()
        # create an sql command string to update textbooks table with new information
        sql = """UPDATE Textbooks
                SET TextbookNumber = ? ,
                    TextbookTitle = ? ,
                    TextbookCost = ? ,
                    TextbookCondition = ? ,
                    StudentNumber = ?
                WHERE TextbookId = ?"""
        # execute sql command string with selected textbook as input parameters and close cursor object
        cur.execute(sql, textbook)
        cur.close()
        # commit the changed database
        conn.commit()

def return_textbook(conn, TextbookNumber, TextbookCondition):
    # find student number and withdrawl condition of the returned textbook
    StudentNumber = ""
    for textbook in get_textbooks(conn):
        if textbook[1] == TextbookNumber:
            StudentNumber = textbook[5]
            WithdrawlCondition = textbook[4]
            break
    # create an sql command string
    sql_cmd = """INSERT INTO ReturnedTextbooks(TextbookNumber, StudentNumber, WithdrawlCondition, ReturnCondition)
                 VALUES (?,?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (TextbookNumber, StudentNumber, WithdrawlCondition, TextbookCondition))
    # commit the changes to the database
    conn.commit()
    # return true to indicate that the operation has been successfuly applied
    cur.close()

def get_returned_textbooks(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("SELECT * FROM ReturnedTextbooks WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

def insert_course(conn, CourseNumber, CourseName, CourseTeacher):
    # create an sql command string
    sql_cmd = """INSERT INTO Courses(CourseNumber, CourseName, CourseTeacher, CourseTextbooks)
                 VALUES (?,?,?,?)"""
    # create a cursor object
    cur = conn.cursor()
    # execute the sql command string using the function parameters
    cur.execute(sql_cmd, (CourseNumber, CourseName, CourseTeacher, ""))
    # commit the changes to the database
    conn.commit()
    # return the id of the inserted course
    CourseId = cur.lastrowid
    cur.close()
    return CourseId

def set_course_requisites(conn, CourseNumber, CourseRequisites):
    for c in get_courses(conn):
        if c[1] == CourseNumber:
            course = c
    sql_cmd = """UPDATE Courses
                 SET CourseTextbooks = ?
                 WHERE CourseId = ?"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (CourseRequisites, course[0]))
    conn.commit()

def get_courses(conn):
    # create a cursor object
    cur = conn.cursor()
    # execute an sql command string
    cur.execute("select * FROM Courses WHERE 1")
    # return the results of the query
    result = cur.fetchall()
    cur.close()
    return result

def reset_excel_data(conn):
    # create a cursor object
    cur = conn.cursor()
    cur.execute("DELETE FROM Students;")
    cur.execute("DELETE FROM Courses;")
    cur.close()

# function to import students from enrollment sheet of formated excel document (SampleData.xlsx)
def import_students(conn, sheets_filename):
    # open enrollments sheet
    enrollment = xlrd.open_workbook(sheets_filename).sheet_by_index(0)
    # insert students into database
    student_numbers = []
    for i in range(1, enrollment.nrows):
        if enrollment.cell_value(i, 0) not in student_numbers:
            insert_student(conn, str(int(enrollment.cell_value(i, 0))), enrollment.cell_value(i, 2)+" "+enrollment.cell_value(i, 3), "0")
            student_numbers.append(enrollment.cell_value(i, 0))
    # add courses to students in database
    student_courses = {}
    for i in range(1, enrollment.nrows):
        if str(int(enrollment.cell_value(i, 0))) in student_courses:
            student_courses[str(int(enrollment.cell_value(i, 0)))].append(str(enrollment.cell_value(i, 4)).split(".")[0]+"."+str(int(enrollment.cell_value(i, 5))))
        else:
            student_courses[str(int(enrollment.cell_value(i, 0)))] = [str(enrollment.cell_value(i, 4)).split(".")[0]+"."+str(int(enrollment.cell_value(i, 5)))]
    for StudentNumber in student_courses.keys():
        for s in get_students(conn):
            if s[1] == StudentNumber:
                student = list(s)
                break
        if student:
            student[4] = "|".join(student_courses[StudentNumber])
            student.append(student[0])
            student = student[1:]
            cur = conn.cursor()
            sql_cmd = """UPDATE Students
                         SET StudentNumber = ? ,
                             StudentName = ? ,
                             StudentDeposit = ? ,
                             StudentCourses = ?
                         WHERE StudentId = ?"""
            cur.execute(sql_cmd, student)
            cur.close()
            conn.commit()


# function to import courses from enrollments sheet and teachers sheet
def import_courses(conn, sheets_filename):
    # open enrollments, courses, and teachers sheets
    enrollment = xlrd.open_workbook(sheets_filename).sheet_by_index(0)
    courses = xlrd.open_workbook(sheets_filename).sheet_by_index(1)
    teachers = xlrd.open_workbook(sheets_filename).sheet_by_index(2)
    # insert courses into database
    course_identifiers = []
    for i in range(1, enrollment.nrows):
        if str(enrollment.cell_value(i, 4)).split(".")[0]+"."+str(int(float(enrollment.cell_value(i, 5)))) not in course_identifiers:
            # find teacher name
            for j in range(1, teachers.nrows):
                if teachers.cell_value(j, 2) == enrollment.cell_value(i, 6):
                    teacher_name = teachers.cell_value(j, 0)+" "+teachers.cell_value(j, 1)
            # find course name
            for j in range(1, courses.nrows):
                if courses.cell_value(j, 1) == enrollment.cell_value(i, 4):
                    course_name = courses.cell_value(j, 0)
            insert_course(conn, str(enrollment.cell_value(i, 4)).split(".")[0]+"."+str(int(float(enrollment.cell_value(i, 5)))), course_name, teacher_name)
            course_identifiers.append(str(enrollment.cell_value(i, 4)).split(".")[0]+"."+str(int(float(enrollment.cell_value(i, 5)))))

