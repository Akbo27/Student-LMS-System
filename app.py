from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

STUDENT_DB = "db/students.db"
CREDITS_DB = "db/credits.db"

if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form["name"] 
        student_id = request.form["student_id"]

        conn = sqlite3.connect(STUDENT_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name = ? AND student_id = ?", (name, student_id))
        student = cursor.fetchone()
        conn.close()

        if student:
            session["student_id"] = student_id
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = sqlite3.connect(STUDENT_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name, major, credits_earned, entry_date, graduation_date FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        return redirect(url_for("login"))

    name, major, credits_earned, entry_date, graduation_date = student

    conn = sqlite3.connect(CREDITS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT computer_science, data_science, interaction_design, high_tech_entrepreneurship, digital_marketing FROM credits WHERE student_id = ?", (student_id,))
    credits = cursor.fetchone()
    conn.close()

    pie_chart_path = None
    if credits:
        credit_labels = ["CS", "DS", "ID", "HTE", "DM"]
        credit_values = list(credits)

        plt.figure(figsize=(6, 6))
        plt.pie(credit_values, labels=credit_labels, autopct="%1.1f%%", 
                colors=["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0"])
        plt.title(f"{name}'s Credit Distribution")
        
        pie_chart_path = f"static/pie_chart_{student_id}.png"
        plt.savefig(pie_chart_path)
        plt.close()

    return render_template("dashboard.html", name=name, major=major, credits_earned=credits_earned,
                           entry_date=entry_date, graduation_date=graduation_date, 
                           credit_values=credits, student_id=student_id, pie_chart=pie_chart_path)

if __name__ == "__main__":
    app.run(debug=True)