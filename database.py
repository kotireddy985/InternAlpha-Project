import sqlite3

conn = sqlite3.connect("bank.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    balance REAL
)
""")

conn.commit()

conn.close()

print("Database Created Successfully")