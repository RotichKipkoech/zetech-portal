from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from forms import LoginForm, CreateStudentForm, CreateFinanceForm, AddFeeForm, PostUnitForm, EditUserForm
from models import db, User, Student, Finance, Unit, StudentFee

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
    
    # Determine the time-based greeting
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"
    
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
    
    return render_template('login.html', form=form, greeting=greeting)
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
    
    # Query all students
    students = db.session.query(Student, User).join(User, Student.user_id == User.id).all()

   
    # Query all finance users by joining User and Finance tables
    finance_users = db.session.query(User, Finance).join(Finance).filter(User.role == 'Finance').all()

    return render_template('admin_dashboard.html', students=students, finance_users=finance_users)


@app.route('/student_dashboard')
@login_required
def student_dashboard():
    # Ensure that only students can access this route
    if current_user.role != 'Student':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    # Fetch the student record associated with the current user
    student = Student.query.filter_by(user_id=current_user.id).first()

    # If student exists, fetch their fees
    if student:
        # Get all fees related to the student
        fees = StudentFee.query.filter_by(student_id=student.id).all()
        
        # Calculate the fee balance (amount due - amount paid)
        fee_balance = sum(fee.amount_due - fee.amount_paid for fee in fees)
    else:
        # If no student record is found, set balance to 0
        fee_balance = 0

    # Render the student dashboard template with fee_balance passed as a context
    return render_template('student_dashboard.html', fee_balance=fee_balance)


@app.route('/finance_dashboard', methods=['GET', 'POST'])
@login_required
def finance_dashboard():
    form = AddFeeForm()
    # Access student's name through the related User model
    form.student_id.choices = [(s.id, s.user.username) for s in Student.query.join(User).all()]

    if form.validate_on_submit():
        student_id = form.student_id.data
        amount_due = form.amount.data
        due_date = datetime.utcnow()  # Example; you may want to use a form field for this
        
        # Create and add the fee entry
        fee = StudentFee(student_id=student_id, amount_due=amount_due, due_date=due_date)
        db.session.add(fee)
        db.session.commit()
        flash('Fee added successfully', 'success')
        return redirect(url_for('finance_dashboard'))

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
        username = form.username.data
        password = form.password.data
        admission_number = form.admission_number.data

        # Create User for Student
        user = User(username=username, role='Student', password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Create Student using the newly created user_id
        student = Student(user_id=user.id, admission_number=admission_number)
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
        username = form.username.data
        password = form.password.data
        staff_number = form.staff_number.data

        # Check if staff_number already exists
        existing_finance_user = Finance.query.filter_by(staff_number=staff_number).first()
        if existing_finance_user:
            flash("This staff number is already in use. Please choose a different one.", 'danger')
            return redirect(url_for('add_finance_user'))

        # Create User for Finance staff
        user = User(username=username, role='Finance', password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Create Finance using the newly created user_id
        finance_user = Finance(user_id=user.id, staff_number=staff_number)
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


@app.route('/add_fee/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_fee(student_id):
    form = AddFeeForm()
    if form.validate_on_submit():
        amount_due = form.amount.data
        due_date = date.today()  # Or specify the due date as needed
        # Create a new StudentFee record for the student
        student_fee = StudentFee(student_id=student_id, amount_due=amount_due, due_date=due_date)
        db.session.add(student_fee)
        db.session.commit()
        flash('Fee successfully added!', 'success')
        return redirect(url_for('finance_dashboard'))
    return render_template('add_fee.html', form=form)
@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    student = Student.query.filter_by(user_id=user_id).first()
    finance = Finance.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        # Update user details
        user.username = request.form['username']
        new_password = request.form['password']
        
        if new_password:
            user.set_password(new_password)  # Assuming `set_password` handles hashing

        # Update student-specific details
        if student:
            student.admission_number = request.form['admission_number']
        
        # Update finance-specific details
        if finance:
            finance.staff_number = request.form['staff_number']

        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred while updating user: {str(e)}', 'danger')

    return render_template('edit_user.html', user=user, student=student, finance=finance)


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'Admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)

    try:
        # Check and delete associated student record, if it exists
        student = Student.query.filter_by(user_id=user_id).first()
        if student:
            db.session.delete(student)
        
        # Check and delete associated finance record, if it exists
        finance = Finance.query.filter_by(user_id=user_id).first()
        if finance:
            db.session.delete(finance)

        db.session.delete(user)  # Finally, delete the user after dependencies are removed
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error occurred while deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))



# General dashboard route for other users
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
