import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="DANI",
    database="myhealthtracker",

)

mycursor = mydb.cursor()

try:
  # Increase timeout value (optional, already done previously)
  # mycursor.execute("SET SESSION wait_timeout = 28800")
  # mycursor.execute("SET SESSION interactive_timeout = 28800")
  mycursor.execute("OPTIMIZE TABLE User_Tests")
  # Read any results (optional)
  mycursor.fetchall()
  mydb.commit()
  print("Table optimized successfully")
except mysql.connector.Error as err:
  print(f"Error optimizing table: {err}")
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()