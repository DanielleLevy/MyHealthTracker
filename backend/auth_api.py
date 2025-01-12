from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS  # ייבוא CORS

app = Flask(__name__)
CORS(app)  # אפשרי CORS לכל היישום


# פונקציה להתחברות למסד הנתונים
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="DANI",
        database="myhealthtracker",
        cursorclass=pymysql.cursors.DictCursor
    )

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
