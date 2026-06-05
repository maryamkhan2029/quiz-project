from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os

from admin import admin_bp
from certificate import generate_certificate

app = Flask(__name__)
app.secret_key = "secretkey123"

app.register_blueprint(admin_bp, url_prefix="/admin")

# ---------------- DATABASE PATH FIX ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
QUIZ_DB = os.path.join(BASE_DIR, "quiz.db")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/quiz")

        return "Invalid login"

    return render_template("login.html")


# ---------------- QUIZ ----------------
@app.route("/quiz")
def quiz():
    conn = sqlite3.connect(QUIZ_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    questions = c.fetchall()
    conn.close()

    return render_template("quiz.html", questions=questions)


# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():
    conn = sqlite3.connect(QUIZ_DB)
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    data = c.fetchall()
    conn.close()

    score = 0

    for i, q in enumerate(data):
        user_answer = request.form.get(str(i))
        if user_answer == q[6]:
            score += 1

    total = len(data)
    wrong = total - score
    percentage = round((score / total) * 100, 2) if total > 0 else 0

    status = "PASS" if percentage >= 50 else "FAIL"
    remark = "Good Work" if percentage >= 50 else "Need Improvement"

    session["last_score"] = score
    session["total"] = total

    return render_template(
        "result.html",
        score=score,
        total=total,
        wrong=wrong,
        percentage=percentage,
        status=status,
        remark=remark
    )


# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
def certificate():
    user = session.get("user", "Student")
    score = session.get("last_score", 0)
    total = session.get("total", 0)

    file_path = generate_certificate(user, score, total)

    return send_file(file_path, as_attachment=True)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ❌ IMPORTANT: VERCEL COMPATIBLE (NO app.run)