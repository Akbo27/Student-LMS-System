from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "your_secret_key"  

if not os.path.exists('static'):
    os.makedirs('static')

DB_PATH = "db/student.db"  

def check_student(name, student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name=? AND student_id=?", (name, student_id))
    student = cursor.fetchone()
    conn.close()
    return student

def get_student_data(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, major, earned_ects, gpa, entry_date, graduation_date FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student 

def generate_pie_chart(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    credits_by_major = {
        "Computer Science": 12,
        "Interaction Design": 20,
        "Data Science": 8,
        "Digital Marketing": 4
    }

    labels = list(credits_by_major.keys())
    sizes = list(credits_by_major.values())

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.axis('equal')  
    pie_path = "static/pie_chart.png"
    plt.savefig(pie_path)
    conn.close()
    return pie_path

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        student_id = request.form["student_id"]

        student = check_student(name, student_id)

        if student:
            session["student_id"] = student[2] 
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid name or student ID")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "student_id" in session:
        student_id = session["student_id"]
        student = get_student_data(student_id)

        if student:
            pie_chart_path = generate_pie_chart(student_id)
            return render_template("dashboard.html", name=student[0], major=student[1], earned_ects=student[2], 
                                   gpa=student[3], entry_date=student[4], graduation_date=student[5], 
                                   pie_chart=pie_chart_path)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
