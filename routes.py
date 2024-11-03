from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
from forms import RegistrationForm, LoginForm, TaskForm
from datetime import datetime

app = Blueprint('app', __name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.passcode.data)
        user = User(username=form.username.data, passcode=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.passcode, form.passcode.data):
            login_user(user)
            return redirect(url_for('app.my_tasks'))
        flash('Invalid username or passcode.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.login'))

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            category=request.form.get('category', ''),
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('app.my_tasks'))
    return render_template('add_task.html', form=form)

@app.route('/my_tasks', methods=['GET'])
@login_required
def my_tasks():
    search_query = request.args.get('search', '')
    tasks = Task.query.filter(Task.user_id == current_user.id)
    if search_query:
        tasks = tasks.filter(Task.title.ilike(f"%{search_query}%"))
    tasks = tasks.order_by(Task.due_date).all()
    return render_template('my_tasks.html', tasks=tasks, count=len(tasks))
