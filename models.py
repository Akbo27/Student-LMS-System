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
        major TEXT NOT NULL
    )
''')

def insert_default_students():
    students_data = [
        ("Aung Kaung Bo", "HSBKK1001", "Computer Science"),
        ("Sai Khay Khun Mong", "HSBKK1002", "Computer Science"),
        ("Nyein Chan Soe", "HSBKK1003", "Computer Science"),
        ("Tom Everson", "HSBKK1004", "Data Science"),
        ("Phone Myint Myat", "HSBKK1005", "Digital Marketing"),
        ("Yang Paing Aung", "HSBKK1006", "Interaction Design"),
        ("Min Myat Swan Pyae", "HSBKK1007", "High Tech Entrepreneurship")
    ]

    cursor.executemany("INSERT OR IGNORE INTO students (name, student_id, major) VALUES (?, ?, ?)", students_data)
    conn.commit()

insert_default_students()

conn.close()