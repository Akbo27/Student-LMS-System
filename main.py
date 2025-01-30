from flask import Flask, render_template, request, redirect, session
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secret_key"

def get_db_connection():
    conn = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form["student_id"]

        conn = get_db_connection()
        student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
        conn.close()

        if student:
            session["student_id"] = student["student_id"]
            return redirect("/dashboard")
        else:
            return "Student ID not found. Please try again."

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE student_id = ?", (session["student_id"],)).fetchone()
    courses = conn.execute("SELECT * FROM courses WHERE student_id = ?", (session["student_id"],)).fetchall()
    conn.close()

    course_labels = [course["course_name"] for course in courses]
    course_values = [course["credits"] for course in courses]

    plt.figure(figsize=(5, 5))
    plt.pie(course_values, labels=course_labels, autopct='%1.1f%%', startangle=90)
    plt.title("Credits Earned per Course")
    plt.savefig("static/credits_chart.png")
    plt.close()

    return render_template("dashboard.html", student=student, courses=courses)

if __name__ == "__main__":
    app.run(debug=True)
