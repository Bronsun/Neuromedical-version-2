from datetime import datetime
import string
from random import choices
from neuro import db ,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(60),unique=False,nullable=False,server_default='patient')
    confirmed = db.Column(db.Boolean, nullable=False, server_default='False')
    confirmed_on = db.Column(db.DateTime, nullable=True,server_default=db.func.now(), server_onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    days = db.relationship('Day', backref='user', lazy=True)
    user_days = db.relationship('UserDay', backref='user', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True)
    memory = db.relationship('Memory', backref='user', lazy=True)
    problems = db.relationship('Problem', backref='user', lazy=True)

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    active =  db.Column(db.Boolean, nullable=False, server_default='True')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_day = db.relationship('UserDay', backref='day', lazy=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    day_texts = db.relationship('DayText', backref='day', lazy=True)

class UserDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class DayText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
class Math(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
class Memory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    score = db.Column(db.Text, unique=False, nullable=True)
    time = db.Column(db.Text,unique=False,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    text = db.Column(db.String(4000), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), unique=False, nullable=True)
    text = db.Column(db.String(255), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(60),unique=False,nullable=False,server_default='Admin')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

db.create_all()