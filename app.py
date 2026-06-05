from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register")
def register():
    return "Register page working"

# ---------------- LOGIN ----------------
@app.route("/login")
def login():
    return "Login page working"

# ---------------- QUIZ (TEMP SAFE) ----------------
@app.route("/quiz")
def quiz():
    return "Quiz page working (Supabase removed for fix)"

# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():
    return "Submit working"

# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
def certificate():
    return "Certificate working"

# ---------------- VERCEL ENTRY ----------------
app = app