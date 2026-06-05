from flask import Flask, render_template, request, redirect, session
from supabase import create_client

app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------------- SUPABASE ----------------
SUPABASE_URL = "https://kofuudhozedguvbuxpcl.supabase.co"
SUPABASE_KEY = "PASTE_YOUR_ANON_PUBLIC_KEY_HERE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

        try:
            supabase.table("users").insert({
                "username": username,
                "password": password
            }).execute()
        except Exception as e:
            return f"Register Error: {str(e)}"

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = supabase.table("users") \
                .select("*") \
                .eq("username", username) \
                .eq("password", password) \
                .execute()

            if user.data:
                session["user"] = username
                return redirect("/quiz")

            return "Invalid login"

        except Exception as e:
            return f"Login Error: {str(e)}"

    return render_template("login.html")

# ---------------- QUIZ ----------------
@app.route("/quiz")
def quiz():
    try:
        data = supabase.table("questions").select("*").execute()
        questions = data.data

        if not questions:
            return "No questions found"

        return render_template("quiz.html", questions=questions)

    except Exception as e:
        return f"Quiz Error: {str(e)}"

# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = supabase.table("questions").select("*").execute()
        questions = data.data

        score = 0

        for i, q in enumerate(questions):
            user_answer = request.form.get(str(i))
            if user_answer == q["correct"]:
                score += 1

        total = len(questions)
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

    except Exception as e:
        return f"Submit Error: {str(e)}"

# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
def certificate():
    user = session.get("user", "Student")
    score = session.get("last_score", 0)
    total = session.get("total", 0)

    return f"""
    <h2>Certificate of Completion</h2>
    <p>Student: {user}</p>
    <p>Score: {score}/{total}</p>
    <p>Congratulations!</p>
    """

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- VERCEL ENTRY ----------------
app = app