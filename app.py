from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, CreateStudentForm, CreateFinanceForm, AddFeeForm, PostUnitForm
from models import db, User, Student, Finance, Unit

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zetech_university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check for Admin credentials
        if form.username.data == "Admin" and form.password.data == "Admin@123":
            admin_user = User.query.filter_by(username="Admin").first()
            if not admin_user:
                # Create Admin user if it does not exist
                admin_user = User(username="Admin", password=generate_password_hash("Admin@123"), role='Admin')
                db.session.add(admin_user)
                db.session.commit()
            
            login_user(admin_user)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Normal user login
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            if user.role == 'Finance':
                return redirect(url_for('finance_dashboard'))
            elif user.role == 'Student':
                return redirect(url_for('student_dashboard'))
            return redirect(url_for('dashboard'))  # Redirect to general user dashboard

        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('admin_dashboard.html', students=students)

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'Student':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    student_units = Unit.query.all()  # Replace with student-specific units if needed
    return render_template('student_dashboard.html', units=student_units)

@app.route('/finance_dashboard', methods=['GET', 'POST'])
@login_required
def finance_dashboard():
    if current_user.role != 'Finance':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    form = AddFeeForm()
    if form.validate_on_submit():
        amount = form.amount.data
        # Logic to handle fee addition (e.g., linking to a student)
        flash("Fee added successfully.")
    finances = Finance.query.all()
    return render_template('finance_dashboard.html', form=form, finances=finances)

@app.route('/admin/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    form = CreateStudentForm()
    if form.validate_on_submit():
        name = form.name.data
        admission_number = form.admission_number.data
        student = Student(name=name, admission_number=admission_number)
        db.session.add(student)
        db.session.commit()
        flash("Student created successfully.")
        return redirect(url_for("admin_dashboard"))
    return render_template("create_student.html", form=form)

@app.route('/admin/add_finance_user', methods=['GET', 'POST'])
@login_required
def add_finance_user():
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    form = CreateFinanceForm()
    if form.validate_on_submit():
        name = form.name.data
        staff_number = form.staff_number.data
        finance_user = Finance(name=name, staff_number=staff_number)
        db.session.add(finance_user)
        db.session.commit()
        flash("Finance user created successfully.")
        return redirect(url_for("admin_dashboard"))
    return render_template("create_finance_user.html", form=form)

@app.route('/admin/add_unit', methods=['GET', 'POST'])
@login_required
def add_unit():
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    form = PostUnitForm()
    if form.validate_on_submit():
        unit_name = form.name.data
        unit = Unit(unit_name=unit_name)
        db.session.add(unit)
        db.session.commit()
        flash("Unit added successfully.")
        return redirect(url_for("admin_dashboard"))
    return render_template("create_unit.html", form=form)

# General dashboard route for other users
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
