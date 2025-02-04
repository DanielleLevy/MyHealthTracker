import pandas as pd
import pymysql
import random
import datetime


# התחברות למסד הנתונים
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="DANI",
    database="myhealthtracker"
)
#file path
#csv_file = "../data/2015.csv"
#csv_file = "../data/2016.csv"
#csv_file = "../data/2017.csv"
#csv_file = "../data/2018.csv"
#csv_file = "../data/2019.csv"
csv_file = "../data/2020.csv"

# test columns to be inserted to the DB
test_columns = [
    "BP_HIGH", "BP_LWST", "BLDS", "TOT_CHOLE", "TRIGLYCERIDE",
    "HDL_CHOLE", "LDL_CHOLE", "CREATININE", "HMG",
    "OLIG_PROTE_CD", "SGOT_AST", "SGPT_ALT", "GAMMA_GTP"
]

# age group to age range mapping
age_group_to_range = {
    1: (0, 4), 2: (5, 9), 3: (10, 14), 4: (15, 19),
    5: (20, 24), 6: (25, 29), 7: (30, 34), 8: (35, 39),
    9: (40, 44), 10: (45, 49), 11: (50, 54), 12: (55, 59),
    13: (60, 64), 14: (65, 69), 15: (70, 74), 16: (75, 79), 17: (80, 84), 18: (85, 100)
}
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def generate_age(age_group):
    age_range = age_group_to_range.get(age_group, (0, 0))
    return random.randint(age_range[0], age_range[1])

def process_chunk(chunk):
    with connection.cursor() as cursor:
        print(f"Processing chunk with {len(chunk)} rows...")

        # Batch Insert ל-Users
        user_data = [
            (row['IDV_ID'], f'pass{row["IDV_ID"]}', row['AGE'], row['SEX'],
             row['WEIGHT'], row['HEIGHT'], row['AGE_GROUP'])
            for _, row in chunk.iterrows()
        ]
        for user in user_data:
            print(f"Preparing to add/update user: {user[0]} with age: {user[2]}")

        user_query = """
        INSERT INTO Users (username, password, age, gender, weight, height, age_group)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE age = VALUES(age), weight = VALUES(weight), height = VALUES(height);
        """
        cursor.executemany(user_query, user_data)

        # Batch Insert to User_Tests
        for test in test_columns:
            if test in chunk.columns:
                test_data = chunk[["IDV_ID", "DATE", test]].dropna(subset=[test])
                test_data = test_data.rename(columns={test: "value"})
                test_data["test_name"] = test
                # filter out invalid dates
                test_data = test_data[test_data['DATE'].apply(is_valid_date)]
                # update date format
                test_data['DATE'] = pd.to_datetime(test_data['DATE'], errors='coerce').dt.strftime('%Y-%m-%d')

                batch_data = [(row['IDV_ID'], row['test_name'], row['DATE'], row['value']) for _, row in test_data.iterrows()]
                test_query = """
                INSERT INTO User_Tests (username, test_name, test_date, value)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE value = VALUES(value);
                """
                cursor.executemany(test_query, batch_data)

        connection.commit()


try:
    print(f"Processing file: {csv_file}")
    data = pd.read_csv(csv_file)

#random values for the missing data
    data['AGE'] = data['AGE_GROUP'].apply(generate_age)
    print("Sample of calculated AGE values:")
    print(data[['IDV_ID', 'AGE_GROUP', 'AGE']].head(10))

#data split to chunks
    chunk_size = 10000
    chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


    for chunk in chunks:
        process_chunk(chunk)

    print("File processed successfully!")

finally:
    connection.close()
    print("Connection closed.")
