import sqlite3


db = sqlite3.connect('database\\main.db')

cur = db.cursor()

with open('database\\schema.sql', 'r') as f:
    file_content = f.read()
    print(file_content)
    db.cursor().executescript(file_content)

db.commit()
