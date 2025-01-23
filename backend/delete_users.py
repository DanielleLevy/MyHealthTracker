import pymysql


def delete_user_tests_in_batches(batch_size=1000):
    # התחברות למסד הנתונים
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="DANI",
        database="myhealthtracker",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # יצירת טבלה זמנית
            cursor.execute("""
                CREATE TEMPORARY TABLE TempUsersToDelete (
                    username VARCHAR(255)
                )
            """)

            while True:
                # הכנסת משתמשים לטבלה הזמנית
                cursor.execute(f"""
                    INSERT INTO TempUsersToDelete (username)
                    SELECT username
                    FROM UsersToDelete
                    LIMIT {batch_size}
                """)

                # בדיקה אם יש עוד משתמשים למחוק
                if cursor.rowcount == 0:
                    print("No more users to delete.")
                    break

                # מחיקת בדיקות
                cursor.execute("""
                    DELETE FROM User_Tests
                    WHERE username IN (SELECT username FROM TempUsersToDelete)
                """)
                print(f"Deleted {cursor.rowcount} records from User_Tests.")

                # מחיקת המשתמשים מטבלת UsersToDelete
                cursor.execute("""
                    DELETE FROM UsersToDelete
                    WHERE username IN (SELECT username FROM TempUsersToDelete)
                """)
                print(f"Deleted {cursor.rowcount} users from UsersToDelete.")

                # ניקוי הטבלה הזמנית
                cursor.execute("TRUNCATE TABLE TempUsersToDelete")

                # שמירת השינויים
                connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()


# קריאה לפונקציה
delete_user_tests_in_batches(batch_size=500)
