from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate  # Import Flask-Migrate
from models import db, init_app, User  # Import models and db
import os

# Create the Flask application
app = Flask(__name__)

# Enable CORS
CORS(app)

# Database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/myhealthtracker.db'
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the database
init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create the database if it doesn't exist (using migrations for future updates)
with app.app_context():
    db.create_all()

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "age": user.age} for user in users])

# Route to add a new user
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

# Home route
@app.route('/')
def home():
    return "Welcome to MyHealthTracker!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
