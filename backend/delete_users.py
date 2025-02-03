import pymysql


def delete_user_tests_in_batches(batch_size=1000):

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="DANI",
        database="myhealthtracker",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # create a temporary table to store users to delete
            cursor.execute("""
                CREATE TEMPORARY TABLE TempUsersToDelete (
                    username VARCHAR(255)
                )
            """)

            while True:
                # insert users to delete into the temporary table
                cursor.execute(f"""
                    INSERT INTO TempUsersToDelete (username)
                    SELECT username
                    FROM UsersToDelete
                    LIMIT {batch_size}
                """)

                # check if there are any users to delete
                if cursor.rowcount == 0:
                    print("No more users to delete.")
                    break

                # delete user tests
                cursor.execute("""
                    DELETE FROM User_Tests
                    WHERE username IN (SELECT username FROM TempUsersToDelete)
                """)
                print(f"Deleted {cursor.rowcount} records from User_Tests.")

                # delete users from UsersToDelete
                cursor.execute("""
                    DELETE FROM UsersToDelete
                    WHERE username IN (SELECT username FROM TempUsersToDelete)
                """)
                print(f"Deleted {cursor.rowcount} users from UsersToDelete.")

                # clear the temporary table
                cursor.execute("TRUNCATE TABLE TempUsersToDelete")

                # save the changes
                connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()



delete_user_tests_in_batches(batch_size=500)
