from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS  # ייבוא CORS
from datetime import datetime, date
import joblib
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
                SELECT u.username, u.age, u.gender, u.weight, u.height,u.age_group, 
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
@app.route('/api/predict_diabetes', methods=['GET'])
def predict_diabetes():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # מיפוי קבוצות גיל
    age_group_mapping = {
        1: (18, 24), 2: (25, 29), 3: (30, 34), 4: (35, 39),
        5: (40, 44), 6: (45, 49), 7: (50, 54), 8: (55, 59),
        9: (60, 64), 10: (65, 69), 11: (70, 74), 12: (75, 79),
        13: (80, 100)
    }

    # שלב 1: שליפת נתוני המשתמש ממסד הנתונים
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שליפת נתוני Life_style ונתוני משתמש כלליים
            cursor.execute("""
                SELECT 
                    Users.age,
                    Users.height,
                    Users.weight,
                    Users.gender, 
                    Life_style.smoking,
                    Life_style.drinking,
                    Life_style.physical_activity,
                    Life_style.education_levels
                FROM Users
                LEFT JOIN Life_style ON Users.username = Life_style.user_username
                WHERE Users.username = %s
            """, (username,))
            user_data = cursor.fetchone()

            if not user_data:
                return jsonify({"error": "User not found"}), 404

            # שלב 2: שליפת בדיקות (BP_HIGH, BP_LWST, TOT_CHOLE) מ-User_Tests
            cursor.execute("""
                SELECT 
                    test_name, value
                FROM User_Tests
                WHERE username = %s AND test_name IN ('BP_HIGH', 'BP_LWST', 'TOT_CHOLE')
            """, (username,))
            test_data = cursor.fetchall()

            # עיבוד בדיקות לשליפה מהירה לפי שם
            test_values = {row['test_name']: float(row['value']) for row in test_data}

            # בדיקה שכל הנתונים קיימים
            if 'BP_HIGH' not in test_values or 'BP_LWST' not in test_values or 'TOT_CHOLE' not in test_values:
                return jsonify({"error": "Missing test data for blood pressure or cholesterol"}), 400

        # שלב 3: חישוב והתאמות נתונים
        # 3.1: חישוב BMI
        if user_data['height'] and user_data['weight']:
            height_in_meters = user_data['height'] / 100
            BMI = round(user_data['weight'] / (height_in_meters ** 2), 2)
        else:
            return jsonify({"error": "Missing height or weight for BMI calculation"}), 400

        # 3.2: מיפוי גיל לקבוצת גיל
        age = user_data['age']
        age_group = next((group for group, (min_age, max_age) in age_group_mapping.items() if min_age <= age <= max_age), None)
        if not age_group:
            return jsonify({"error": "Age is out of range"}), 400

        # 3.3: חישוב לחץ דם גבוה
        HighBP = 1 if (test_values['BP_HIGH'] > 140 or test_values['BP_LWST'] > 90) else 0

        # 3.4: חישוב כולסטרול גבוה
        HighChol = 1 if test_values['TOT_CHOLE'] > 200 else 0

        # 3.5: מיפוי עישון ל-0/1
        Smoker = 1 if user_data['smoking'] in [2, 3] else 0

        # 3.6: מיפוי פעילות גופנית ל-0/1
        PhysActivity = 1 if user_data['physical_activity'] in [2, 3] else 0

        # 3.7: מיפוי שתייה ל-0/1
        HvyAlcoholConsump = 1 if user_data['drinking'] == 1 else 0

        # שלב 4: הכנת הפיצ'רים למודל
        features = [
            HighBP,           # לחץ דם גבוה
            HighChol,         # כולסטרול גבוה
            BMI,              # BMI
            Smoker,           # עישון
            PhysActivity,     # פעילות גופנית
            HvyAlcoholConsump, # שתייה
            user_data['gender'],
            user_data['education_levels'],  # רמת השכלה
            age_group         # קבוצת גיל
        ]

        # שלב 5: טעינת המודל
        import joblib
        model_path = '../models/best_diabetes_model_Gradient Boosting.pkl'
        diabetes_model = joblib.load(model_path)
        print(f"User data fetched: {user_data}")
        print(f"Prepared features: {features}")

        # שלב 6: חיזוי
        prediction = diabetes_model.predict([features])[0]
        probability = diabetes_model.predict_proba([features])[0][int(prediction)]

        # שלב 7: תרגום התוצאה לתגובה למשתמש
        risk_mapping = {
            0: "Low Risk of Diabetes",
            1: "Moderate Risk (Pre-Diabetes)",
            2: "High Risk of Diabetes"
        }
        result = {
            "risk_level": risk_mapping.get(prediction, "Unknown"),
            "probability": round(probability * 100, 2)  # סיכוי באחוזים
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()
@app.route('/api/predict_stroke', methods=['GET'])
def predict_stroke():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # שלב 1: שליפת נתוני המשתמש ממסד הנתונים
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שליפת נתוני Life_style ונתוני משתמש כלליים
            cursor.execute("""
                SELECT 
                    Users.gender,
                    Users.age,
                    Users.height,
                    Users.weight,
                    Life_style.smoking,
                    User_Tests.value AS avg_glucose_level,
                    User_Tests.test_name
                FROM Users
                LEFT JOIN Life_style ON Users.username = Life_style.user_username
                LEFT JOIN User_Tests ON Users.username = User_Tests.username
                WHERE Users.username = %s AND User_Tests.test_name = 'BLDS'
            """, (username,))
            user_data = cursor.fetchone()

            if not user_data:
                return jsonify({"error": "User not found"}), 404

            # שלב 2: שליפת בדיקות לחץ דם מ-User_Tests
            cursor.execute("""
                SELECT 
                    test_name, value
                FROM User_Tests
                WHERE username = %s AND test_name IN ('BP_HIGH', 'BP_LWST')
            """, (username,))
            bp_data = cursor.fetchall()

            # עיבוד בדיקות לשליפה מהירה לפי שם
            bp_values = {row['test_name']: float(row['value']) for row in bp_data}

            # בדיקה שכל הנתונים קיימים
            if 'BP_HIGH' not in bp_values or 'BP_LWST' not in bp_values:
                return jsonify({"error": "Missing blood pressure data"}), 400

        # שלב 3: חישוב והתאמות נתונים
        # 3.1: מיפוי מגדר
        gender_mapping = {"Male": 1, "Female": 2, "Other": 3}
        gender = gender_mapping.get(user_data['gender'], 3)  # ערך ברירת מחדל: 3 (Other)

        # 3.2: חישוב BMI
        if user_data['height'] and user_data['weight']:
            height_in_meters = user_data['height'] / 100
            BMI = round(user_data['weight'] / (height_in_meters ** 2), 2)
        else:
            return jsonify({"error": "Missing height or weight for BMI calculation"}), 400

        # 3.3: חישוב יתר לחץ דם
        hypertension = 1 if (bp_values['BP_HIGH'] > 140 or bp_values['BP_LWST'] > 90) else 0

        # 3.4: מיפוי עישון ל-0/1
        smoking_status_mapping = {1: 1, 2: 2, 3: 3, 0: 0}
        smoking_status = smoking_status_mapping.get(user_data['smoking'], 0)

        # 3.5: מיפוי סטטוס נישואין
        ever_married_mapping = {"Yes": 2, "No": 1}
        ever_married = ever_married_mapping.get(user_data.get('ever_married', "No"), 1)

        # 3.6: רמת גלוקוז ממוצעת
        avg_glucose_level = user_data.get('avg_glucose_level', 0)

        # שלב 4: הכנת הפיצ'רים למודל
        features = [
            gender,             # מגדר
            user_data['age'],   # גיל
            hypertension,       # יתר לחץ דם
            ever_married,       # סטטוס נישואין
            avg_glucose_level,  # רמת גלוקוז ממוצעת
            BMI,                # BMI
            smoking_status      # עישון
        ]

        # שלב 5: טעינת המודל
        import joblib
        model_path = '../models/best_stroke_model_Logistic Regression.pkl'
        stroke_model = joblib.load(model_path)
        print(f"User data fetched: {user_data}")
        print(f"Prepared features: {features}")

        # שלב 6: חיזוי
        prediction = stroke_model.predict([features])[0]
        probability = stroke_model.predict_proba([features])[0][int(prediction)]

        # שלב 7: תרגום התוצאה לתגובה למשתמש
        risk_mapping = {
            0: "Low Risk of Stroke",
            1: "High Risk of Stroke"
        }
        result = {
            "risk_level": risk_mapping.get(prediction, "Unknown"),
            "probability": round(probability * 100, 2)  # סיכוי באחוזים
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()

@app.route('/api/predict_depression', methods=['GET'])
def predict_depression():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Fetch user data
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    age,
                    marital_status,
                    education_levels,
                    children,
                    smoking,
                    physical_activity,
                    work,
                    drinking,
                    dietary_habit,
                    sleep_pattern
                FROM Users
                LEFT JOIN Life_style ON Users.username = Life_style.user_username
                WHERE Users.username = %s
            """, (username,))
            user_data = cursor.fetchone()

            if not user_data:
                return jsonify({"error": "User not found"}), 404

        # Prepare the input features
        features = [
            user_data['age'],
            user_data['marital_status'],
            user_data['education_levels'],
            user_data['children'],
            1 if user_data['smoking'] in [2, 3] else 0,  # Binary mapping for smoking
            1 if user_data['physical_activity'] in [2, 3] else 0,  # Binary mapping for physical activity
            user_data['work'],
            1 if user_data['drinking'] == 1 else 0,  # Binary mapping for drinking
            user_data['dietary_habit'],
            user_data['sleep_pattern'],
        ]

        # Load the model
        model_path = '../models/best_logistic_regression_model_depression.pkl'  # Update with your model path
        depression_model = joblib.load(model_path)

        # Make prediction
        prediction = depression_model.predict([features])[0]
        probability = depression_model.predict_proba([features])[0][int(prediction)]

        # Map results to readable format
        risk_mapping = {0: "Low Risk", 1: "High Risk"}
        result = {
            "risk_level": risk_mapping.get(prediction, "Unknown"),
            "probability": round(probability * 100, 2)
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()


@app.route('/api/predict_heart_disease', methods=['GET'])
def predict_heart_disease():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # שלב 1: שליפת נתוני המשתמש ממסד הנתונים
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שליפת נתוני Life_style ונתוני משתמש כלליים
            cursor.execute("""
                SELECT 
                    Users.age,
                    Users.gender,
                    Users.height,
                    Users.weight,
                    Life_style.smoking,
                    Life_style.physical_activity,
                    Life_style.drinking,
                    User_Tests.test_name,
                    User_Tests.value
                FROM Users
                LEFT JOIN Life_style ON Users.username = Life_style.user_username
                LEFT JOIN User_Tests ON Users.username = User_Tests.username
                WHERE Users.username = %s AND User_Tests.test_name IN ('BP_HIGH', 'BP_LWST', 'TOT_CHOLE', 'BLDS')
            """, (username,))
            user_data = cursor.fetchall()

            if not user_data:
                return jsonify({"error": "User not found"}), 404

            # עיבוד נתוני הבדיקות לשליפה מהירה לפי שם
            test_values = {row['test_name']: float(row['value']) for row in user_data}

            # בדיקה שכל הנתונים הנדרשים קיימים
            required_tests = ['BP_HIGH', 'BP_LWST', 'TOT_CHOLE', 'BLDS']
            if not all(test in test_values for test in required_tests):
                return jsonify({"error": "Missing required test data"}), 400

        # שלב 2: חישוב והתאמות נתונים
        # 2.1: חישוב גיל (אם יש)
        age = user_data[0]['age']

        # 2.2: מיפוי מגדר
        # Updated gender mapping for your data
        gender_mapping = {1: 1, 2: 0}  # 1 = Male, 0 = Female
        gender = gender_mapping.get(user_data[0]['gender'], 0)

        # 2.3: חישוב לחץ דם במנוחה
        resting_blood_pressure = test_values['BP_HIGH']  # ניתן להשתמש ב-BP_HIGH בלבד

        # 2.4: כולסטרול בדם
        cholesterol = test_values['TOT_CHOLE']

        # 2.5: סוכר בצום
        fasting_blood_sugar = 1 if test_values['BLDS'] > 120 else 0

        # 2.6: מיפוי עישון ל-0/1
        smoking_mapping = {1: 0, 2: 1, 3: 1}
        smoking = smoking_mapping.get(user_data[0]['smoking'], 0)

        # 2.7: מיפוי פעילות גופנית
        physical_activity = user_data[0]['physical_activity']

        # שלב 3: הכנת הפיצ'רים למודל
        features = [
            age,                # גיל
            gender,             # מגדר
            resting_blood_pressure,  # לחץ דם במנוחה
            cholesterol,        # כולסטרול
            fasting_blood_sugar # סוכר בצום
        ]

        # שלב 4: טעינת המודל
        import joblib
        model_path = '../models/best_heart_disease_model.pkl'
        heart_disease_model = joblib.load(model_path)
        print(f"User data fetched: {user_data}")
        print(f"Prepared features: {features}")

        # שלב 5: חיזוי
        prediction = heart_disease_model.predict([features])[0]
        probability = heart_disease_model.predict_proba([features])[0][int(prediction)]

        # שלב 6: תרגום התוצאה לתגובה למשתמש
        risk_mapping = {
            0: "Low Risk of Heart Disease",
            1: "High Risk of Heart Disease"
        }
        result = {
            "risk_level": risk_mapping.get(prediction, "Unknown"),
            "probability": round(probability * 100, 2)  # סיכוי באחוזים
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        connection.close()

@app.route('/api/compare_tests', methods=['GET'])
def compare_tests():
    connection = get_db_connection()
    smoking = request.args.get('smoking')
    drinking = request.args.get('drinking')
    physical_activity = request.args.get('physical_activity')
    education_levels = request.args.get('education_levels')
    age_group = request.args.get('age_group')

    if not all([smoking, drinking, physical_activity, education_levels, age_group]):
        return jsonify({"error": "Missing required parameters"}), 400

    query = """
   SELECT 
    ut.test_name,
    AVG(ut.value) AS avg_value,
    STDDEV(ut.value) AS std_dev,
    MIN(ut.value) AS min_value,
    MAX(ut.value) AS max_value,
    tv.lower_limit,
    tv.upper_limit,
    JSON_ARRAYAGG(FLOOR(ut.value / 10) * 10) AS histogram
FROM 
    User_Tests ut
JOIN 
    Users u ON ut.username = u.username
JOIN 
    Life_style ls ON u.username = ls.user_username
JOIN 
    Tests_Values tv ON ut.test_name = tv.test_name
JOIN (SELECT username FROM Users ORDER BY RAND() LIMIT 1000) AS random_users ON u.username = random_users.username -- שימוש ב-JOIN
WHERE 
    ls.smoking = %s
    AND ls.drinking = %s
    AND ls.physical_activity = %s
    AND ls.education_levels = %s
    AND tv.age_group = %s
GROUP BY 
    ut.test_name, tv.lower_limit, tv.upper_limit;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (smoking, drinking, physical_activity, education_levels, age_group))
            results = cursor.fetchall()

        # בדיקת היסטוגרמות ריקות
        for result in results:
            if not result['histogram']:
                print(f"Warning: Histogram for test {result['test_name']} is empty.")
        print("Results from database:", results)  # הדפסה חשובה!

        return jsonify(results), 200
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/comparison_analysis', methods=['GET'])
def comparison_analysis():
    connection = get_db_connection()

    # קבלת פרמטרים מהבקשה
    smoking = request.args.get('smoking')
    drinking = request.args.get('drinking')
    physical_activity = request.args.get('physical_activity')
    education_levels = request.args.get('education_levels')
    age_group = request.args.get('age_group')

    # בדיקה שכל הפרמטרים הדרושים קיימים
    if not all([smoking, drinking, physical_activity, education_levels, age_group]):
        return jsonify({"error": "Missing required parameters"}), 400

    # שאילתת SQL לחישוב הערכים הממוצעים ותוצאות השוואתיות
    query = """
    SELECT 
        ut.test_name,
        AVG(ut.value) AS avg_value,
        STDDEV(ut.value) AS std_dev,
        MIN(ut.value) AS min_value,
        MAX(ut.value) AS max_value,
        tv.lower_limit,
        tv.upper_limit
    FROM 
        User_Tests ut
    JOIN 
        Users u ON ut.username = u.username
    JOIN 
        Life_style ls ON u.username = ls.user_username
    JOIN 
        Tests_Values tv ON ut.test_name = tv.test_name
    WHERE 
        ls.smoking = %s
        AND ls.drinking = %s
        AND ls.physical_activity = %s
        AND ls.education_levels = %s
        AND tv.age_group = %s
    GROUP BY 
        ut.test_name, tv.lower_limit, tv.upper_limit;
    """

    try:
        # ביצוע השאילתה
        print(f"Executing query with parameters: {smoking}, {drinking}, {physical_activity}, {education_levels}, {age_group}")
        with connection.cursor() as cursor:
            cursor.execute(query, (smoking, drinking, physical_activity, education_levels, age_group))
            results = cursor.fetchall()
            print("Query Results:", results)  # דיבוג: הדפסת התוצאות
        return jsonify(results), 200
    except Exception as e:
        print("Error executing query:", e)  # הדפסת שגיאה
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/get_tests', methods=['GET'])
def get_tests():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שאילתא לשליפת שם ותיאור של הבדיקות
            cursor.execute("SELECT test_name, full_name, description FROM Tests")
            tests = cursor.fetchall()
            print("API output:", tests)  # הדפסת המידע בקונסול לבדיקה
        return jsonify({'tests': tests}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
@app.route('/api/get_test_limits', methods=['GET'])
def get_test_limits():
    username = request.args.get('username')
    test_name = request.args.get('test_name')

    if not username or not test_name:
        return jsonify({"error": "Username and test_name are required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # שליפת קבוצת הגיל של המשתמש
            cursor.execute("SELECT age_group FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found"}), 404

            age_group = user['age_group']

            # שליפת המינימום והמקסימום עבור הבדיקה וקבוצת הגיל
            cursor.execute("""
                SELECT lower_limit, upper_limit 
                FROM Tests_Values 
                WHERE test_name = %s AND age_group = %s
            """, (test_name, age_group))
            limits = cursor.fetchone()

            if not limits:
                return jsonify({"error": "Limits not found for the given test and age group"}), 404

            return jsonify({"lower_limit": limits['lower_limit'], "upper_limit": limits['upper_limit']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
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

        return jsonify({"success": True, "alerts": alerts}), 200

    except Exception as e:
        print(f"Error fetching health alerts: {str(e)}")  

    finally:
        cursor.close()
        connection.close()

@app.route('/api/user_test_summary', methods=['GET'])
def get_user_test_summary():
    username = request.args.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Get the user's age group
            cursor.execute("SELECT age_group FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            age_group_id = user['age_group']

            # Get the latest test results for the user with normal ranges
            cursor.execute("""
                SELECT 
                    t.test_name, 
                    ts.full_name,
                    t.test_date, 
                    t.value, 
                    v.lower_limit, 
                    v.upper_limit 
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

            if not test_results:
                return jsonify({'tests': []}), 200

            tests_summary = []
            for test in test_results:
                test_name = test['full_name']
                last_test_date = test['test_date']

                # Ensure last_test_date is converted to a datetime object
                if isinstance(last_test_date, date):
                    last_test_date = datetime.combine(last_test_date, datetime.min.time())

                test_value = float(test['value']) if test['value'] else None
                lower_limit = float(test['lower_limit']) if test['lower_limit'] else None
                upper_limit = float(test['upper_limit']) if test['upper_limit'] else None

                # Determine if value is out of range
                is_out_of_range = (
                    (upper_limit is not None and test_value > upper_limit) or
                    (lower_limit is not None and test_value < lower_limit)
                )

                # Determine if the test is overdue (>1 year)
                is_overdue = (datetime.now() - last_test_date).days > 365

                test_data = {
                    'test_name': test_name,
                    'latest_value': test_value,
                    'min_range': lower_limit,
                    'max_range': upper_limit,
                    'last_test_date': last_test_date.strftime('%Y-%m-%d'),
                    'is_out_of_range': is_out_of_range,
                    'is_overdue': is_overdue
                }
                tests_summary.append(test_data)

            return jsonify({'tests': tests_summary}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

@app.route('/api/update_lifestyle_info', methods=['POST'])
def update_lifestyle():
    data = request.json
    username = data.get("username")
    marital_status = data.get("marital_status")
    education_levels = data.get("education_levels")
    children = data.get("children")
    physical_activity = data.get("physical_activity")
    work = data.get("work")
    dietary_habit = data.get("dietary_habit")
    sleep_pattern = data.get("sleep_pattern")
    drinking = data.get("drinking")
    smoking = data.get("smoking")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Life_style (user_username, marital_status, education_levels, children, physical_activity, work, dietary_habit, sleep_pattern, drinking, smoking)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                marital_status=VALUES(marital_status),
                education_levels=VALUES(education_levels),
                children=VALUES(children),
                physical_activity=VALUES(physical_activity),
                work=VALUES(work),
                dietary_habit=VALUES(dietary_habit),
                sleep_pattern=VALUES(sleep_pattern),
                drinking=VALUES(drinking),
                smoking=VALUES(smoking)
            """, (username, marital_status, education_levels, children, physical_activity, work, dietary_habit, sleep_pattern, drinking, smoking))
            connection.commit()
        return jsonify({"message": "Lifestyle information updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/api/get_lifestyle_info', methods=['GET'])
def get_lifestyle():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Life_style WHERE user_username = %s", (username,))
            row = cursor.fetchone()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)