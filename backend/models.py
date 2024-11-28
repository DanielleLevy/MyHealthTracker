from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID ייחודי
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)

class Test(db.Model):
    test_name = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    description = db.Column(db.Text)

class UserTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # קשר לטבלת משתמשים
    test_name = db.Column(db.String(255))  # שם הבדיקה
    test_date = db.Column(db.Date)  # תאריך הבדיקה
    value = db.Column(db.Float)  # ערך הבדיקה

class MentalHealth(db.Model):
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True, nullable=False)
    history_mental_illness = db.Column(db.Boolean)
    history_abuse = db.Column(db.Boolean)
    family_depression = db.Column(db.Boolean)
    chronic_condition = db.Column(db.Boolean)

class LifeStyle(db.Model):
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True, nullable=False)
    smoking = db.Column(db.Boolean)
    drinking = db.Column(db.Boolean)
    physical_activity = db.Column(db.Integer)
    marital_status = db.Column(db.Integer)
    work = db.Column(db.Boolean)
    education_levels = db.Column(db.Integer)
    children = db.Column(db.Integer)
    sleep_pattern = db.Column(db.Integer)
    dietary_habit = db.Column(db.Integer)
