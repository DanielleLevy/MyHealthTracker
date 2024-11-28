from app import app
print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
import os
import kagglehub
import pandas as pd
from models import db, User, UserTest
from datetime import datetime

# התחלת ההקשר של האפליקציה
with app.app_context():
    # הורדת נתוני Health Checkup
    health_path = kagglehub.dataset_download("hongseoi/health-checkup-result")
    print("Health Checkup Dataset Path:", health_path)

    # עיבוד קבצים בתיקייה
    for file_name in os.listdir(health_path):
        if file_name.endswith('.csv'):
            print(f"Processing file: {file_name}")
            file_path = os.path.join(health_path, file_name)
            health_data = pd.read_csv(file_path)

            # עיבוד שורות
            for _, row in health_data.iterrows():
                try:
                    # בדיקה אם המשתמש כבר קיים
                    user = User.query.filter_by(id=row['IDV_ID']).first()
                    if not user:
                        # יצירת username ייחודי על בסיס ID
                        generated_username = f"user_{row['IDV_ID']}"

                        user = User(
                            id=row['IDV_ID'],
                            username=generated_username,  # יצירת שם משתמש דינמי
                            password="default_password",  # סיסמת ברירת מחדל
                            age=row.get('AGE', None),
                            gender=row.get('GENDER', None),
                            weight=row.get('WEIGHT', None),
                            height=row.get('HEIGHT', None),
                            bmi=row.get('BMI', None)
                        )
                        db.session.add(user)

                    # הוספת בדיקות משתמש
                    test = UserTest(
                        user_id=user.id,
                        test_name="Health Checkup",
                        test_date=f"{file_name.split('.')[0]}-01-01",
                        value=row.get('VALUE', None)  # טיפול בערך חסר
                    )
                    db.session.add(test)

                except Exception as e:
                    print(f"Error processing row: {row} | Error: {e}")

            # שמירת השינויים למסד הנתונים לאחר כל קובץ
            db.session.commit()
            print(f"Processed {file_name} successfully!")
