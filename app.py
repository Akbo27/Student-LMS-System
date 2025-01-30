from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  
DB_PATH = "db/student.db" 

def check_student(name, student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name=? AND student_id=?", (name, student_id))
    student = cursor.fetchone()
    conn.close()
    return student 

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        student_id = request.form["student_id"]

        student = check_student(name, student_id)

        if student:
            session["name"] = student[1]  
            session["student_id"] = student[2]  
            session["major"] = student[3]  
            return redirect("/dashboard")  
        else:
            return render_template("login.html", error="Invalid name or student ID")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], student_id=session["student_id"], major=session["major"])
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
