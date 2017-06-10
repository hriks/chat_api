from flask import render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,\
    login_user, login_required, logout_user, current_user
from .. import app, User, db, Group
from forms import LoginForm, RegisterForm
from flask import session, request
from . import main

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if 'logged' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                admin = User.query.filter_by(
                    username=str(user.username)
                ).first()
                admin.is_active = True
                db.session.commit()
                session['logged'] = 'YES'
                if current_user:
                    return redirect(url_for('dashboard'))
                return redirect(url_for('login'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        admin = User.query.filter_by(
            username=str(new_user.username)
        ).first()
        admin.is_active = True
        db.session.commit()

        return redirect(url_for('dashboard'))
    flash('Please Signup to view')
    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    users = User.query.order_by(User.username)
    groups = Group.query.order_by(Group.username)
    return render_template(
        'dashboard.html',
        name=current_user.username,
        users=users,
        groups=groups
    )


@app.route('/logout')
@login_required
def logout():
    user = User.query.filter_by(username=str(current_user.username)).first()
    user.is_active = False
    db.session.commit()
    session.clear()
    logout_user()
    return redirect(url_for('index'))
