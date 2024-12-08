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

from models import db, User
from app import app

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}")


import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../instance/myhealthtracker.db')  # Adjust path if needed
cursor = conn.cursor()

# Step 1: Create a new 'life_style' table with 'user_id' ForeignKey referencing 'user.id'
cursor.execute(
CREATE TABLE life_style_new (
    user_id INTEGER PRIMARY KEY,
    smoking BOOLEAN,
    drinking BOOLEAN,
    physical_activity INTEGER,
    marital_status INTEGER,
    work BOOLEAN,
    education_levels INTEGER,
    children INTEGER,
    sleep_pattern INTEGER,
    dietary_habit INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
)

# Step 2: Copy data from the old 'life_style' table to the new one
cursor.execute(
INSERT INTO life_style_new (user_id, smoking, drinking, physical_activity, marital_status, work, education_levels, children, sleep_pattern, dietary_habit)
SELECT user_username, smoking, drinking, physical_activity, marital_status, work, education_levels, children, sleep_pattern, dietary_habit
FROM life_style;
)

# Step 3: Drop the old 'life_style' table
cursor.execute("DROP TABLE life_style;")

# Step 4: Rename the new table to 'life_style'
cursor.execute("ALTER TABLE life_style_new RENAME TO life_style;")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("ForeignKey updated successfully!")
"""

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../instance/myhealthtracker.db')
cursor = conn.cursor()

# Inspect columns in the 'life_style' table
cursor.execute("PRAGMA table_info(life_style);")
columns = cursor.fetchall()
print("Columns in 'life_style':", columns)

conn.close()
