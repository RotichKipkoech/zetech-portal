from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association Table for Student and Unit Many-to-Many Relationship
student_units = db.Table('student_units',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('unit_id', db.Integer, db.ForeignKey('units.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128))  # Changed to 'password'

    def __init__(self, username, role, password):
        self.username = username
        self.role = role
        self.password = password  # Changed to 'password'

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    finance_id = db.Column(db.Integer, db.ForeignKey('finances.id'), nullable=True)

    finance = db.relationship('Finance', back_populates='students')
    units = db.relationship('Unit', secondary=student_units, back_populates='students')
    fees = db.relationship('StudentFee', back_populates='student')

    def __init__(self, name, admission_number, finance_id=None):
        self.name = name
        self.admission_number = admission_number
        self.finance_id = finance_id

class Finance(db.Model):
    __tablename__ = 'finances'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    students = db.relationship('Student', back_populates='finance')

    def __init__(self, name):
        self.name = name

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    students = db.relationship('Student', secondary=student_units, back_populates='units')

    def __init__(self, name):
        self.name = name

class StudentFee(db.Model):
    __tablename__ = 'student_fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False, default=0)
    due_date = db.Column(db.Date, nullable=False)

    student = db.relationship('Student', back_populates='fees')

    def __init__(self, student_id, amount_due, due_date):
        self.student_id = student_id
        self.amount_due = amount_due
        self.due_date = due_date
