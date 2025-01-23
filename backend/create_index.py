import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="DANI",
    database="myhealthtracker",

)
mycursor = mydb.cursor()

try:
    # יצירת אינדקסים
    index_queries = [
        "ALTER TABLE Users ADD INDEX idx_username (username);",
        "ALTER TABLE User_Tests ADD INDEX idx_username_testname (username, test_name);",
        "ALTER TABLE Life_style ADD INDEX idx_user_lifestyle (user_username, smoking, drinking, physical_activity, education_levels);",
        "ALTER TABLE Tests_Values ADD INDEX idx_testname_agegroup (test_name, age_group);"
    ]

    for query in index_queries:
        print(f"Executing query: {query}")  # הדפסה לניטור
        mycursor.execute(query)
        mydb.commit()
        print("Index created successfully.")

    print("All indexes created successfully!")

except mysql.connector.Error as err:
    print(f"Error creating indexes: {err}")
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()