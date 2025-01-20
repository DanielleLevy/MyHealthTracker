from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS  # ייבוא CORS

app = Flask(__name__)
CORS(app)  # אפשרי CORS לכל היישום
@app.route('/api/user_data', methods=['GET'])
def get_user_data():
    username = request.args.get('username')  # לדוגמה, המשתמש המחובר

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    connection = get_db_connection()  # יצירת חיבור למסד הנתונים
    try:
        with connection.cursor() as cursor:
            # עדכון השאילתה לכלול את education_levels
            cursor.execute("""
                SELECT u.username, u.age, u.gender, u.weight, u.height, 
                       l.smoking, l.drinking, l.physical_activity, l.education_levels
                FROM Users u
                LEFT JOIN Life_style l ON u.username = l.user_username
                WHERE u.username = %s
            """, (username,))
            user_data = cursor.fetchone()  # הבאת רשומה אחת בלבד

        # בדיקה אם המשתמש קיים
        if not user_data:
            return jsonify({'error': 'User not found'}), 404

        # חישוב BMI (אם גובה ומשקל קיימים)
        if user_data['height'] and user_data['weight']:
            height_in_meters = user_data['height'] / 100
            user_data['BMI'] = round(user_data['weight'] / (height_in_meters ** 2), 2)
        else:
            user_data['BMI'] = "N/A"

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
 # סגירת החיבור


# פונקציה להתחברות למסד הנתונים
def get_db_connection():
    return pymysql.connect(
        host="192.168.0.215",
        user="team_user",
        password="123",
        database="myhealthtracker",
        cursorclass=pymysql.cursors.DictCursor
    )
@app.route('/api/add_test', methods=['POST'])
def add_test():
    data = request.json
    username = data.get('username')
    test_name = data.get('test_name')
    test_date = data.get('test_date')
    value = data.get('value')

    if not username or not test_name or not test_date:
        return jsonify({'error': 'Missing required fields'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # הוספת רשומה חדשה לטבלת User_Tests
            cursor.execute(
                "INSERT INTO User_Tests (username, test_name, test_date, value) VALUES (%s, %s, %s, %s)",
                (username, test_name, test_date, value)
            )
        connection.commit()
        return jsonify({'success': True, 'message': 'Test added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/api/get_user_tests', methods=['GET'])
def get_user_tests():
    username = request.args.get('username')  # קבלת שם המשתמש מהבקשה
    if not username:
        return jsonify({"error": "Username not provided"}), 400  # אם שם המשתמש לא סופק, החזרת שגיאה

    connection = get_db_connection()  # יצירת חיבור למסד הנתונים
    try:
        with connection.cursor() as cursor:
            # שאילתא לשליפת הבדיקות של המשתמש
            query = "SELECT * FROM User_Tests WHERE username = %s ORDER BY test_date DESC"
            cursor.execute(query, (username,))
            tests = cursor.fetchall()  # שליפת כל הרשומות

        return jsonify({"tests": tests}), 200  # החזרת הבדיקות בפורמט JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # החזרת שגיאה במקרה של בעיה
    finally:
        connection.close()  # סגירת החיבור למסד הנתונים


@app.route('/api/compare_tests', methods=['GET'])
def compare_tests():
    smoking = request.args.get('smoking')
    drinking = request.args.get('drinking')
    physical_activity = request.args.get('physical_activity')
    education_levels = request.args.get('education_levels')

    if not (smoking and drinking and physical_activity and education_levels):
        return jsonify({'error': 'Missing lifestyle parameters'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                test_name,
                AVG(value) AS avg_value,
                STDDEV(value) AS std_dev_value,
                MIN(value) AS min_value,
                MAX(value) AS max_value
            FROM 
                User_Tests
            JOIN 
                Life_style ON User_Tests.username = Life_style.user_username
            WHERE 
                smoking = %s AND
                drinking = %s AND
                physical_activity = %s AND
                education_levels = %s
            GROUP BY 
                test_name
            """
            cursor.execute(query, (smoking, drinking, physical_activity, education_levels))
            basic_result = cursor.fetchall()

            # הכנת התפלגות (distribution) לכל בדיקה
            results = []
            for row in basic_result:
                test_name = row['test_name']
                min_value = row['min_value']
                max_value = row['max_value']

                # חלוקת הטווח ל-10 סלים
                bin_size = (max_value - min_value) / 10
                bins = [min_value + i * bin_size for i in range(11)]

                # ספירת מספר המשתמשים בכל סל
                distribution_query = """
                SELECT 
                    FLOOR((value - %s) / %s) AS bin,
                    COUNT(*) AS count
                FROM 
                    User_Tests
                WHERE 
                    test_name = %s AND
                    value BETWEEN %s AND %s
                GROUP BY bin
                """
                cursor.execute(distribution_query, (min_value, bin_size, test_name, min_value, max_value))
                distribution_data = cursor.fetchall()

                # הפקת התפלגות כ-list
                distribution = [0] * 10
                for bin_data in distribution_data:
                    bin_index = int(bin_data['bin'])
                    if 0 <= bin_index < 10:
                        distribution[bin_index] = bin_data['count']

                results.append({
                    'test_name': test_name,
                    'avg_value': row['avg_value'],
                    'std_dev_value': row['std_dev_value'],
                    'min_value': min_value,
                    'max_value': max_value,
                    'distribution': distribution,
                })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

@app.route('/api/get_tests', methods=['GET'])
def get_tests():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שאילתא לשליפת רשימת הבדיקות עם השם המלא שלהן
            cursor.execute("SELECT test_name, full_name FROM Tests")
            tests = cursor.fetchall()

        # החזרת רשימת הבדיקות כולל שם הבדיקה המלא
        return jsonify({'tests': tests}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# פונקציה לטיפול בהתחברות
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print("Received data:", data)  # לוג לבדיקת הנתונים שהגיעו לשרת

    username = data.get('username')
    password = data.get('password')

    # בדיקת שם משתמש וסיסמה
    if not username or not password:
        print("Missing username or password")  # לוג לשגיאה
        return jsonify({"error": "Username and password are required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # ביצוע שאילתה
            cursor.execute(
                "SELECT * FROM Users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            print("Query result:", user)  # לוג לתוצאות השאילתה

        # אם המשתמש נמצא
        if user:
            print("Login successful for user:", username)  # לוג להתחברות מוצלחת
            return jsonify({"success": True, "user": user}), 200
        else:
            print("Invalid username or password")  # לוג להתחברות כושלת
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
    finally:
        connection.close()



@app.route('/api/update_user_info', methods=['POST'])
def update_user_info():
    data = request.json
    username = data.get('username')
    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Users 
                SET age = %s, height = %s, weight = %s
                WHERE username = %s
            """, (age, height, weight, username))

        connection.commit()
        return jsonify({'success': True, 'message': 'User information updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

def get_age_group(age):
    age_group_to_range = {
        1: (0, 4), 2: (5, 9), 3: (10, 14), 4: (15, 19),
        5: (20, 24), 6: (25, 29), 7: (30, 34), 8: (35, 39),
        9: (40, 44), 10: (45, 49), 11: (50, 54), 12: (55, 59),
        13: (60, 64), 14: (65, 69), 15: (70, 74), 16: (75, 79),
        17: (80, 84), 18: (85, 100)
    }
    
    for group, (min_age, max_age) in age_group_to_range.items():
        if min_age <= age <= max_age:
            return group
    return None  # במקרה שהגיל לא נמצא בטווחים


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    height = data.get('height')
    weight = data.get('weight')
    age = data.get('age')
    gender = data.get('gender') 

    age_group = get_age_group(age)

    if not (username and password and age and gender is not None):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # בדיקה אם שם המשתמש כבר קיים
            cursor.execute("SELECT username FROM Users WHERE username = %s", (username,))
            if cursor.fetchone():
                return jsonify({"success": False, "message": "Username already exists"}), 400

            cursor.execute("""
                INSERT INTO Users (username, password, height, weight, age, age_group, gender) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, password, height, weight, age, age_group, gender))
            
        connection.commit()
        return jsonify({"success": True, "message": "User registered successfully", "user": username}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()

@app.route('/api/user_health_alerts', methods=['GET'])
def get_health_alerts():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Missing required fields"}), 400
    
    print(f"Fetching health alerts for user '{username}'")
    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        # בדיקת קבוצת גיל
        cursor.execute("SELECT age_group FROM Users WHERE username = %s", (username))
        user = cursor.fetchone()

        if not user:
            print(f"User '{username}' not found in Users table")
            return jsonify({"success": False, "message": "User not found"}), 404
        
        age_group_id = user['age_group']
        print(f"User '{username}' belongs to age group {age_group_id}")

        # בדיקת בדיקות אחרונות לכל test_name
        cursor.execute("""
            SELECT t.test_name, ts.full_name, t.test_date, t.value, v.lower_limit, v.upper_limit 
            FROM User_Tests t
            JOIN Tests_Values v ON t.test_name = v.test_name 
            JOIN Tests ts ON t.test_name = ts.test_name 
            WHERE t.username = %s AND v.age_group = %s
            AND t.test_date = (
                SELECT MAX(t2.test_date) 
                FROM User_Tests t2 
                WHERE t2.username = t.username AND t2.test_name = t.test_name
            )
            ORDER BY t.test_date DESC
        """, (username, age_group_id))

        test_results = cursor.fetchall()
        print(f"Test results found for user '{username}': {test_results}")

        if not test_results:
            print(f"No test results found for user '{username}' in age group {age_group_id}")
            return jsonify({"success": True, "alerts": []}), 200

        alerts = []
        for test in test_results:
            test_name = test['full_name']

            # ערכים מתוך מסד הנתונים
            try:
                test_value = float(test['value']) if test['value'] is not None else None
                lower_limit = float(test['lower_limit']) if test['lower_limit'] is not None else None
                upper_limit = float(test['upper_limit']) if test['upper_limit'] is not None else None

            except ValueError as ve:
                print(f"ValueError for test {test_name}: {str(ve)}")
                continue

            # בדיקה אם יש חריגה
            if upper_limit is not None and test_value > upper_limit:
                alerts.append(f"High {test_name} detected!")
            if lower_limit is not None and test_value < lower_limit:
                alerts.append(f"Low {test_name} detected!")

        print(f"Alerts generated for user '{username}': {alerts}")

        return jsonify({"success": True, "alerts": alerts}), 200

    except Exception as e:
        print(f"Error fetching health alerts: {str(e)}")  # ✅ הדפסת השגיאה
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
