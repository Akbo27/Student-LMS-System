import sqlite3
import os

STUDENT_DB = "db/students.db"
CREDITS_DB = "db/credits.db"
GRADES_DB = "db/student_grades.db" 

os.makedirs("db", exist_ok=True)

def create_student_table():
    conn = sqlite3.connect(STUDENT_DB)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        student_id TEXT UNIQUE NOT NULL,
                        major TEXT NOT NULL,
                        credits_earned TEXT DEFAULT '0/180',
                        entry_date TEXT NOT NULL,
                        graduation_date TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

def insert_default_students():
    students_data = [
        ("Aung Kaung Bo", "HSBKK1001", "Computer Science", "44/180", "8 Feb 2023", "27 March 2027"),
        ("Sai Khay Khun Mong", "HSBKK1002", "Computer Science", "30/180", "12 March 2023", "28 Feb 2027"),
        ("Nyein Chan Soe", "HSBKK1003", "Computer Science", "25/180", "20 April 2023", "30 May 2027")
    ]
    
    conn = sqlite3.connect(STUDENT_DB)
    cursor = conn.cursor()
    
    for student in students_data:
        cursor.execute("INSERT OR IGNORE INTO students (name, student_id, major, credits_earned, entry_date, graduation_date) VALUES (?, ?, ?, ?, ?, ?)", student)

    conn.commit()
    conn.close()

def create_credits_table():
    conn = sqlite3.connect(CREDITS_DB)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS credits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT NOT NULL UNIQUE,
                        computer_science INTEGER DEFAULT 0,
                        data_science INTEGER DEFAULT 0,
                        interaction_design INTEGER DEFAULT 0,
                        high_tech_entrepreneurship INTEGER DEFAULT 0,
                        digital_marketing INTEGER DEFAULT 0,
                        FOREIGN KEY (student_id) REFERENCES students(student_id))''')
    
    conn.commit()
    conn.close()

def insert_default_credits():
    credits_data = [
        ("HSBKK1001", 12, 4, 8, 10, 0),
        ("HSBKK1002", 10, 3, 6, 7, 4),
        ("HSBKK1003", 8, 2, 5, 9, 1)
    ]

    conn = sqlite3.connect(CREDITS_DB)
    cursor = conn.cursor()
    
    for credit in credits_data:
        cursor.execute("INSERT OR IGNORE INTO credits (student_id, computer_science, data_science, interaction_design, high_tech_entrepreneurship, digital_marketing) VALUES (?, ?, ?, ?, ?, ?)", credit)

    conn.commit()
    conn.close()

def create_student_grades_table():
    conn = sqlite3.connect(GRADES_DB)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT NOT NULL,
                        major TEXT NOT NULL,
                        module_name TEXT NOT NULL,
                        grade INTEGER CHECK(grade BETWEEN 0 AND 100),
                        FOREIGN KEY (student_id) REFERENCES students(student_id))''')
    
    conn.commit()
    conn.close()

def insert_student_grade(student_id, major, module_name, grade):
    conn = sqlite3.connect(GRADES_DB)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO student_grades (student_id, major, module_name, grade) VALUES (?, ?, ?, ?)", 
                   (student_id, major, module_name, grade))
    
    conn.commit()
    conn.close()

def get_student_grades(student_id):
    conn = sqlite3.connect(GRADES_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT module_name, grade FROM student_grades WHERE student_id = ?", (student_id,))
    grades = cursor.fetchall()
    
    conn.close()
    return grades 

def insert_sample_grades():
    sample_grades = [
        ("HSBKK1001", "Computer Science", "Intro to Python Programming - Part 1", 90),
        ("HSBKK1001", "High Tech Entrepreneurship", "Zero to Hero Module", 85),
        ("HSBKK1001", "Digital Marketing", "Growth Marketing for Startups", 75),
        ("HSBKK1001", "Interaction Design", "Business Innovation Module", 88),
        ("HSBKK1001", "Data Science", "AI & Machine Learning", 92),
        ("HSBKK1001", "Computer Science", "Web Development Bootcamp", 78),
        ("HSBKK1001", "Computer Science", "Cloud Computing Basics", 83)
    ]

    conn = sqlite3.connect(GRADES_DB)
    cursor = conn.cursor()

    for grade in sample_grades:
        cursor.execute("INSERT OR IGNORE INTO student_grades (student_id, major, module_name, grade) VALUES (?, ?, ?, ?)", grade)

    conn.commit()
    conn.close()

create_student_table()
insert_default_students()
create_credits_table()
insert_default_credits()
create_student_grades_table()
insert_sample_grades()