from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, init_app, User  # ייבוא המודלים

# יצירת אפליקציה של Flask
app = Flask(__name__)

CORS(app)

# הגדרות מסד הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/myhealthtracker.db'
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# אתחול מסד הנתונים
init_app(app)

# יצירת מסד הנתונים (אם לא קיים)
with app.app_context():
    db.create_all()

# נקודות קצה
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "age": user.age} for user in users])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        username=data['username'],
        password=data['password'],
        age=data['age']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"})

@app.route('/')
def home():
    return "Welcome to MyHealthTracker!"

# הרצת האפליקציה
if __name__ == '__main__':
    app.run(debug=True)
