from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CreateStudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    submit = SubmitField('Create Student')

class CreateFinanceForm(FlaskForm):
    name = StringField('Finance User Name', validators=[DataRequired()])
    staff_number = StringField('Staff Number', validators=[DataRequired()])
    submit = SubmitField('Create Finance User')

class AddFeeForm(FlaskForm):
    amount = FloatField('Fee Amount', validators=[DataRequired()])
    submit = SubmitField('Add Fee')

class PostUnitForm(FlaskForm):
    name = StringField('Unit Name', validators=[DataRequired()])
    submit = SubmitField('Post Unit')
