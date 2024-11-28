"""

import sqlite3

conn = sqlite3.connect('../instance/myhealthtracker.db')  # עדכני את הנתיב
cursor = conn.cursor()

# בדיקת מבנה הטבלה
cursor.execute("PRAGMA table_info(user);")
columns = cursor.fetchall()
print("Columns in the 'user' table:")
for column in columns:
    print(f"Name: {column[1]}, Type: {column[2]}")

conn.close()

from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    if not users:
        print("The user table is empty.")
    else:
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}")

import sqlite3

conn = sqlite3.connect('../instance/myhealthtracker.db')
cursor = conn.cursor()

# הצגת כל הטבלאות במסד הנתונים
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

conn.close()



import sqlite3

conn = sqlite3.connect('../instance/myhealthtracker.db')
cursor = conn.cursor()

# בדיקת מבנה הטבלה
cursor.execute("PRAGMA table_info(user);")
columns = cursor.fetchall()
print("Columns in 'user':")
for column in columns:
    print(f"Name: {column[1]}, Type: {column[2]}")

conn.close()


import sqlite3

conn = sqlite3.connect('../instance/myhealthtracker.db')
cursor = conn.cursor()

# הצגת כל הטבלאות
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table)

conn.close()


"""
import sqlite3

conn = sqlite3.connect('../instance/myhealthtracker.db')  # ודאי שהנתיב תואם למסד הנתונים שלך
cursor = conn.cursor()

# בדיקת מבנה הטבלה user
cursor.execute("PRAGMA table_info(user);")
columns = cursor.fetchall()
print("Columns in 'user':")
for column in columns:
    print(f"Name: {column[1]}, Type: {column[2]}")

conn.close()
