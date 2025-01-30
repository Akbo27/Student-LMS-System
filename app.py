from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

db_folder = "db"
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

con = sqlite3.connect(f"{db_folder}/student.db")

app = Flask(__name__)
app.secret_key = "your_secret_key"  

def check_student(name, student_id):
    conn = sqlite3.connect("student.db")
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
            session["name"] = name
            session["student_id"] = student_id
            return redirect("/dashboard")  
        else:
            return render_template("login.html", error="Invalid name or student ID")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "name" in session:
        return render_template("dashboard.html", name=session["name"], student_id=session["student_id"])
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)