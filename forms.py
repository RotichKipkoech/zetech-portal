from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CreateStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Student')

class CreateFinanceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    staff_number = StringField('Staff Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Finance User')

class AddFeeForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    amount = FloatField('Fee Amount', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', default=None)  # Optional due date
    submit = SubmitField('Add Fee')

class PostUnitForm(FlaskForm):
    name = StringField('Unit Name', validators=[DataRequired()])
    submit = SubmitField('Post Unit')
    
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Teacher', 'Teacher'), ('Finance', 'Finance'), ('Student', 'Student')], validators=[DataRequired()])
    admission_number = StringField('Admission Number')
    staff_number = StringField('Staff Number')
    submit = SubmitField('Save Changes')