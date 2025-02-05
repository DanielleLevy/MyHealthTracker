import pandas as pd
import pymysql
import random

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="DANI",
    database="myhealthtracker"
)

csv_file = "../data/2015.csv"

# test names to be inserted to the DB
test_columns = [
    "BP_HIGH", "BP_LWST", "BLDS", "TOT_CHOLE", "TRIGLYCERIDE",
    "HDL_CHOLE", "LDL_CHOLE", "CREATININE", "HMG",
    "OLIG_PROTE_CD", "SGOT_AST", "SGPT_ALT", "GAMMA_GTP"
]

try:

    print(f"Processing file: {csv_file}")
    data = pd.read_csv(csv_file)

    # handle missing values
    data['SMK_STAT'] = data['SMK_STAT'].apply(lambda x: 0 if x == 'N' else (1 if x == 'Y' else x))
    data['DRK_YN'] = data['DRK_YN'].apply(lambda x: 0 if x == 'N' else (1 if x == 'Y' else x))
    data['SMK_STAT'] = data['SMK_STAT'].fillna(0).astype(int)
    data['DRK_YN'] = data['DRK_YN'].fillna(0).astype(int)
    data['AGE'] = data['AGE'].fillna(0).astype(int)  

    # check if test columns exist in the CSV
    for col in test_columns:
        if col not in data.columns:
            print(f"Warning: Column {col} not found in CSV!")
        else:
            print(f"Column {col} found. Non-NaN values: {data[col].notna().sum()}")

    # 2. add password column
    data['password'] = data['IDV_ID'].apply(lambda x: f'pass{x}')

    # 3. generate random values for lifestyle columns
    data['marital_status'] = data['IDV_ID'].apply(lambda x: random.choice([1, 2, 3, 4]))
    data['education_levels'] = data['IDV_ID'].apply(lambda x: random.choice([1, 2, 3, 4, 5]))
    data['children'] = data['IDV_ID'].apply(lambda x: random.randint(0, 5))
    data['physical_activity'] = data['IDV_ID'].apply(lambda x: random.choice([1, 2, 3]))
    data['work'] = data['IDV_ID'].apply(lambda x: random.choice([0, 1]))
    data['dietary_habit'] = data['IDV_ID'].apply(lambda x: random.choice([1, 2, 3]))
    data['sleep_pattern'] = data['IDV_ID'].apply(lambda x: random.choice([1, 2, 3]))

    # insert data to DB
    for _, row in data.iterrows():
        # check if user exists
        check_user_query = "SELECT COUNT(*) FROM Users WHERE username = %s"
        with connection.cursor() as cursor:
            cursor.execute(check_user_query, (row['IDV_ID'],))
            user_exists = cursor.fetchone()[0] > 0

        if not user_exists:
            # add user
            user_query = """
            INSERT INTO Users (username, password, age, gender, weight, height, age_group)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(user_query, (
                    row['IDV_ID'], row['password'], row['AGE'], row['SEX'],
                    row['WEIGHT'], row['HEIGHT'], row['AGE_GROUP']
                ))
            connection.commit()
        else:
            print(f"User {row['IDV_ID']} already exists. Updating age.")
            # update age
            update_age_query = """
            UPDATE Users
            SET age = %s
            WHERE username = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(update_age_query, (row['AGE'], row['IDV_ID']))
            connection.commit()

        # update lifestyle
        lifestyle_query = """
        INSERT INTO Life_style (user_username, smoking, drinking, physical_activity, marital_status,
                                work, education_levels, children, sleep_pattern, dietary_habit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        smoking = VALUES(smoking), drinking = VALUES(drinking), 
        physical_activity = VALUES(physical_activity), marital_status = VALUES(marital_status),
        work = VALUES(work), education_levels = VALUES(education_levels), 
        children = VALUES(children), sleep_pattern = VALUES(sleep_pattern), 
        dietary_habit = VALUES(dietary_habit)
        """
        with connection.cursor() as cursor:
            cursor.execute(lifestyle_query, (
                row['IDV_ID'], row['SMK_STAT'], row['DRK_YN'], row['physical_activity'], row['marital_status'],
                row['work'], row['education_levels'], row['children'], row['sleep_pattern'], row['dietary_habit']
            ))
        connection.commit()

    # insert tests data
    for test in test_columns:
        if test in data.columns:
            test_data = data[["IDV_ID", "DATE", test]].dropna(subset=[test])  # filter out NaN values
            test_data = test_data.rename(columns={test: "value"})
            test_data["test_name"] = test
            for _, test_row in test_data.iterrows():
                print(f"Inserting/updating test: {test_row['test_name']} for user {test_row['IDV_ID']}")
                test_query = """
                INSERT INTO User_Tests (username, test_name, test_date, value)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                value = VALUES(value);
                """
                with connection.cursor() as cursor:
                    cursor.execute(test_query, (
                        test_row['IDV_ID'], test_row['test_name'],
                        test_row['DATE'], test_row['value']
                    ))
                connection.commit()

    print("File processed successfully!")

finally:
    connection.close()
    print("Connection closed.")
