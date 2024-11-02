from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Assignment, FeeBalance
from forms import LoginForm, AdminCreateUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zetech.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'Staff':
        return redirect(url_for('staff_dashboard'))
    elif current_user.role == 'Finance':
        return redirect(url_for('finance_dashboard'))
    elif current_user.role == 'Student':
        return redirect(url_for('student_dashboard'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        return redirect(url_for('dashboard'))
    form = AdminCreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'{form.role.data} account created for {form.username.data}', 'success')
    return render_template('admin_dashboard.html', form=form)

@app.route('/staff_dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'Staff':
        return redirect(url_for('dashboard'))
    return render_template('staff_dashboard.html')

@app.route('/finance_dashboard')
@login_required
def finance_dashboard():
    if current_user.role != 'Finance':
        return redirect(url_for('dashboard'))
    return render_template('finance_dashboard.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'Student':
        return redirect(url_for('dashboard'))
    return render_template('student_dashboard.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
