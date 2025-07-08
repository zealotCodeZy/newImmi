from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_member = db.Column(db.Boolean, default=False)
    membership_expires = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_membership_active(self):
        if not self.is_member:
            return False
        if self.membership_expires and self.membership_expires < datetime.utcnow():
            self.is_member = False
            return False
        return True

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    transaction_id = db.Column(db.String(100), unique=True)
    
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

class RentInfo(db.Model):
    __tablename__ = 'rent_info'
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(5), nullable=False)
    address = db.Column(db.String(255))
    content = db.Column(db.Text)

class WorkInfo(db.Model):
    __tablename__ = 'work_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    zipcode = db.Column(db.String(5))
    address = db.Column(db.String(255))
    content = db.Column(db.Text) 