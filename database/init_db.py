# import sqlite3
import mysql.connector


# db = sqlite3.connect('database\\main.db')
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="automated_aquaponics"
)

cur = db.cursor(buffered=True)

with open('schema.sql', 'r') as f:
    file_content = f.read()

    commands = file_content.split(';')
    for command in commands:
        print(command)
        db.cursor().execute(command, multi=True)

db.commit()
