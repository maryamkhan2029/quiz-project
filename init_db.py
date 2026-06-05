import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    a TEXT,
    b TEXT,
    c TEXT,
    d TEXT,
    answer TEXT
)
""")

conn.commit()
conn.close()

print("Database ready")