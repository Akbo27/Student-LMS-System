import sqlite3
import os

if not os.path.exists("db"):
    os.makedirs("db")

conn = sqlite3.connect("db/student.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE NOT NULL,
        major TEXT NOT NULL,
        earned_ects INTEGER DEFAULT 0,
        gpa REAL DEFAULT 0.0,
        entry_date TEXT DEFAULT 'N/A',
        graduation_date TEXT DEFAULT 'N/A'
    )
''')

def insert_default_students():
    students_data = [
        ("Aung Kaung Bo", "HSBKK1001", "Computer Science", 44, 3.7, "April 2024", "March 2027"),
        ("Sai Khay Khun Mong", "HSBKK1002", "Computer Science", 38, 3.5, "May 2023", "April 2026"),
        ("Nyein Chan Soe", "HSBKK1003", "Computer Science", 50, 3.9, "Jan 2024", "Dec 2027"),
        ("Tom Everson", "HSBKK1004", "Data Science", 36, 3.6, "July 2023", "June 2026"),
        ("Phone Myint Myat", "HSBKK1005", "Digital Marketing", 42, 3.4, "Aug 2022", "July 2025"),
        ("Yang Paing Aung", "HSBKK1006", "Interaction Design", 30, 3.2, "Sept 2023", "Aug 2026"),
        ("Min Myat Swan Pyae", "HSBKK1007", "High Tech Entrepreneurship", 48, 3.8, "Oct 2023", "Sept 2026")
    ]

    cursor.executemany("INSERT OR IGNORE INTO students (name, student_id, major, earned_ects, gpa, entry_date, graduation_date) VALUES (?, ?, ?, ?, ?, ?, ?)", students_data)
    conn.commit()

insert_default_students()
conn.close()

print("Database updated with student ECTs, GPA, and dates!")