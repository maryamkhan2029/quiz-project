from flask import Blueprint, render_template, request, redirect, session
import sqlite3

admin_bp = Blueprint("admin", __name__)


# ---------------- LOGIN ----------------
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Wrong login"

    return render_template("admin_login.html")


# ---------------- DASHBOARD ----------------
@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", questions=questions)


# ---------------- ADD ----------------
@admin_bp.route("/add", methods=["GET", "POST"])
def add():
    if not session.get("admin"):
        return redirect("/admin/login")

    if request.method == "POST":
        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO questions (question, a, b, c, d, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["question"],
            request.form["a"],
            request.form["b"],
            request.form["c"],
            request.form["d"],
            request.form["answer"]
        ))

        conn.commit()
        conn.close()

        return redirect("/admin/dashboard")

    return render_template("add_question.html")


# ---------------- DELETE ----------------
@admin_bp.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin/dashboard")


# ---------------- EDIT ----------------
@admin_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE questions
            SET question=?, a=?, b=?, c=?, d=?, answer=?
            WHERE id=?
        """, (
            request.form["question"],
            request.form["a"],
            request.form["b"],
            request.form["c"],
            request.form["d"],
            request.form["answer"],
            id
        ))

        conn.commit()
        conn.close()
        return redirect("/admin/dashboard")

    cursor.execute("SELECT * FROM questions WHERE id=?", (id,))
    q = cursor.fetchone()
    conn.close()

    return render_template("edit_question.html", q=q)


# ---------------- LOGOUT ----------------
@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/admin/login")