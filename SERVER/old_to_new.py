import sqlite3

def insert_student(conn: sqlite3.Connection, number: str, name: str, courses: list):
    """ Insert a student with a given student number, name, and course list
    into the database associated with a given database connection object.
    """
    sql_cmd = """INSERT INTO Students(StudentNumber, StudentName, StudentCourses)
                 VALUES (?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (number, name, "|".join(courses)))
    conn.commit()
    return cur.lastrowid

def add_deposit_change(conn: sqlite3.Connection, date: str, amount: float, student_number: str):
    """ Add a deposit change instance with a given amount to a student in
    in the database associated with a given database connection object.
    """
    sql_cmd = """INSERT INTO DepositChanges(DepositChangeDate, DepositChangeAmount, StudentNumber)
                 VALUES (?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (date, amount, student_number))
    conn.commit()
    return cur.lastrowid

def add_course(conn: sqlite3.Connection, number: str, name: str, teacher: str, textbooks: str):
    """ Add a course with a given course number, name, teacher, and textbook
    list into the databse associated with a given database conection object.
    """
    sql_cmd = """INSERT INTO Courses(CourseNumber, CourseName, CourseTeacher, CourseTextbooks)
                 VALUES(?,?,?,?)"""
    cur =  conn.cursor()
    cur.execute(sql_cmd, (number, name, teacher, "|".join(textbooks)))
    conn.commit()
    return cur.lastrowid

def add_textbook(conn: sqlite3.Connection, title: str, cost: float):
    """ Add a textbook with a given title and cost to the database associated
    with a given database connection object.
    """
    sql_cmd = """INSERT INTO Textbooks(TextbookTitle, TextbookCost)
                 VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (title, cost))
    conn.commit()
    return cur.lastrowid

def add_textbook_instance(conn: sqlite3.Connection, instance_number: str, textbook_id: int):
    """ Add a textbook instance with a given instance number and textbook id
    to the database associated with a given database connection object.
    """
    sql_cmd = """INSERT INTO TextbookInstances(TextbookNumber, TextbookId)
                 VALUES(?,?)"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (instance_number, textbook_id))
    conn.commit()
    return cur.lastrowid

def add_possession_change(conn: sqlite3.Connection, date: str, condition: int, student_number: str, textbook_number: str):
    """ Add a possession change with a given date, condition, student number,
    and textbook number to the database associated with a given database connection
    object.
    """
    sql_cmd = """INSERT INTO PossessionChanges(PossessionChangeDate, PossessionChangeCondition, StudentNumber, TextbookNumber)
                 VALUES(?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql_cmd, (str(date), int(condition), str(student_number), str(textbook_number)))
    conn.commit()
    return cur.lastrowid


if __name__ == "__main__":

    old_conn = sqlite3.connect("server.db")
    new_conn = sqlite3.connect("replacement.db")

    # get old student information
    cur = old_conn.cursor()
    cur.execute("SELECT * FROM Students WHERE 1")
    old_students = cur.fetchall()
    cur.close()

    # get old course information
    cur = old_conn.cursor()
    cur.execute("SELECT * FROM Courses WHERE 1")
    old_courses = cur.fetchall()
    cur.close()

    # get old textbook information
    cur = old_conn.cursor()
    cur.execute("SELECT * FROM Textbooks WHERE 1")
    old_textbooks = cur.fetchall()
    cur.close()

    old_conn.close()
    new_conn.close()
