import sqlite3

conn = sqlite3.connect("symptom_disease.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptoms TEXT,
    predicted_disease TEXT,
    confidence REAL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")
