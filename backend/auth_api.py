from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS  # ייבוא CORS

app = Flask(__name__)
CORS(app)  # אפשרי CORS לכל היישום
@app.route('/api/user_data', methods=['GET'])
def get_user_data():
    # קבלת פרטי המשתמש המחובר (לדוגמה מתוך session או request)
    username = request.args.get('username')  # לדוגמה, המשתמש המחובר

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    connection = get_db_connection()  # יצירת חיבור למסד הנתונים
    try:
        with connection.cursor() as cursor:
            # שאילתא לקבלת נתוני המשתמש הספציפי
            cursor.execute("""
                SELECT u.username, u.age, u.gender, u.weight, u.height, 
                       l.smoking, l.drinking, l.physical_activity
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
        connection.close()  # סגירת החיבור


# פונקציה להתחברות למסד הנתונים
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="DANI",
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
                STDDEV(value) AS std_dev_value
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
            result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/api/get_tests', methods=['GET'])
def get_tests():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שאילתא לשליפת רשימת הבדיקות
            cursor.execute("SELECT DISTINCT test_name FROM User_Tests")
            tests = cursor.fetchall()
        return jsonify({'tests': [test['test_name'] for test in tests]}), 200
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
