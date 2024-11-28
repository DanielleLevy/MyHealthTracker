from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# יצירת אפליקציה של Flask
app = Flask(__name__)

# הגדרות מסד הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myhealthtracker.db'  # שימוש ב-SQLite כמסד נתונים
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # ביטול אזהרות מעקב שינויים

# אתחול SQLAlchemy
db = SQLAlchemy(app)

# יצירת מודלים (טבלאות למסד הנתונים)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # מזהה ייחודי
    name = db.Column(db.String(80), nullable=False)  # שם המשתמש
    email = db.Column(db.String(120), unique=True, nullable=False)  # אימייל ייחודי
    age = db.Column(db.Integer, nullable=False)  # גיל המשתמש

# יצירת מסד הנתונים
with app.app_context():
    db.create_all()  # יצירת הטבלאות אם הן לא קיימות

# נקודת קצה לשליפת משתמשים
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # שליפת כל המשתמשים
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in users])

# נקודת קצה להוספת משתמש חדש
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json  # קבלת נתונים מהבקשה
    new_user = User(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(new_user)  # הוספת המשתמש למסד הנתונים
    db.session.commit()  # שמירת השינויים
    return jsonify({"message": "User added successfully!"})

# נקודת קצה לעמוד הראשי
@app.route('/')
def home():
    return "Welcome to MyHealthTracker!"

# הרצת האפליקציה
if __name__ == '__main__':
    app.run(debug=True)
