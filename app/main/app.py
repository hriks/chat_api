from flask import render_template, redirect, url_for, flash as hriks
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,\
    login_user, login_required, logout_user, current_user
from .. import app, User, db, Group, Group_user
from forms import LoginForm, RegisterForm, GroupForm
from flask import session, request
from sqlalchemy import or_

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
                    hriks(
                        'SUCCESS! Welcome, you are logged in %s' % (
                            user.username
                        )
                    )
                    return redirect(url_for('dashboard'))
                return redirect(url_for('login'))
        hriks(
            'WARNING! Invalid Combination,\
            Please check username and password'
        )
        return render_template('login.html', form=form)

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
        hriks(
            'Notification: Hey, hi %s you are allset, just click and chat!' % (
                new_user.username
            )
        )

        return redirect(url_for('dashboard'))
    hriks('Please Signup to view')
    return render_template('signup.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    users = User.query.order_by(User.username)
    groups = Group.query.order_by(Group.username)
    groups_list = []
    for group in groups:
        groups_list.append(group.group)
    group_set = set(groups_list)
    print group_set
    hriks(
        'Notification: Hey, Hi %s . Welcome ! click to chat.' % (
            current_user.username
        )
    )
    return render_template(
        'dashboard.html',
        name=current_user.username,
        users=users,
        groups=group_set,
        session=session,
    )


@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    group_chat = request.form['submit']
    groups = Group.query.order_by(Group.group)
    for group in groups:
        if group.group == group_chat:
            session['room'] = str(group.group)
    hriks(
        'Notification: Hey, %s you just joined %s' % (
            current_user.username,
            session['room']
        )
    )
    return redirect(url_for('dashboard'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    users = User.query.order_by(User.username)
    group_name = request.form['submit']
    groups = Group.query.order_by(Group.username)
    users_add = []
    for group in groups:
        if group.group == group_name:
            for user in users:
                if user.username == group.username:
                    users_add.append(str(user.username))
                    continue
    all_users = []
    for user in users:
        all_users.append(str(user.username))
    add_users = list(set(all_users) - set(users_add))
    hriks(
        'Notification: Hey, You are currently adding member to group %s' % (
        )
    )
    return render_template(
        'add.html',
        users=add_users,
        group_name=group_name,
    )


@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        group_name = str(request.form['group'])
        member = str(request.form['submit'])
        print member, group_name
        groups = Group.query.order_by(Group.group)
        for group in groups:
            if group_name == group.group and member == group.username:
                userd = 'YES'
            else:
                userd = 'No'
        if userd == 'No':
            group_member = Group(
                group=group_name,
                username=member
            )
            db.session.add(group_member)
            db.session.commit()
        hriks(
            'Notification: Hey, You had just added %s to %s' % (
                member,
                group_name
            )
        )
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))


@app.route('/private_chat', methods=['GET', 'POST'])
@login_required
def private_chat():
    users = User.query.order_by(User.username)
    groups = Group.query.order_by(Group.username)
    groups_list = []
    for group in groups:
        groups_list.append(group.group)
    group_set = set(groups_list)
    if request.method == 'POST':
        name = current_user.username
        session['name'] = str(name)
        room = str(request.form['submit'])
        groups_users = Group_user.query.filter(
            or_(
                Group_user.user1 == current_user.username,
                Group_user.user2 == current_user.username
            )
        )
        for user in groups_users:
            if (
                str(user.user1) == str(
                    current_user.username) and str(
                    user.user2) == room) or (str(
                    user.user1) == room and str(user.user2) == str(
                    current_user.username)
            ):
                userd = 'YES'
                session['room'] = str(user.id)
                break
            else:
                userd = 'No'
        if userd == 'No':
            new_group = Group_user(
                user2=session['name'],
                user1=room
            )
            db.session.add(new_group)
            db.session.commit()
            groups_users = Group_user.query.filter(
                or_(
                    Group_user.user1 == current_user.username,
                    Group_user.user2 == current_user.username
                )
            )
            session['room'] = str(user.id)
        for user in groups_users:
            if (
                str(user.user1) == str(
                    current_user.username) and str(
                    user.user2) == room) or (str(
                    user.user1) == room and str(user.user2) == str(
                    current_user.username)
            ):
                    session['room'] = str(user.id)
    hriks(
        'Notification: You opened chat box with %s' % (
            room
        )
    )
    return render_template(
        'dashboard.html',
        name=current_user.username,
        users=users,
        groups=group_set,
        session=session,
    )


@app.route('/group_chat', methods=['GET', 'POST'])
@login_required
def group_chat():
    form = GroupForm()
    users = User.query.order_by(User.username)

    if form.validate_on_submit():
        if request.method == 'POST':
            name = str(current_user.username)
            print name
            group_name = str(request.form['groupname'])
            print group_name
            member = str(request.form['submit'])
            print member
            group_member1 = Group(
                group=group_name,
                username=name
            )

            db.session.add(group_member1)
            db.session.commit()
            group_member2 = Group(
                group=group_name,
                username=member
            )
            db.session.add(group_member2)
            db.session.commit()
            return redirect(url_for('dashboard'))
    hriks(
        'Notification: You created a group with group name %s and added %s as member' % (    # noqa
            group_name,
            member
        )
    )
    return render_template(
        'group.html',
        form=form,
        session=session,
        users=users
    )


@app.route('/logout')
@login_required
def logout():
    user = User.query.filter_by(username=str(current_user.username)).first()
    user.is_active = False
    db.session.commit()
    session.clear()
    hriks(
        'Notification: %s Successfully Logged out' % (
            current_user.username
        )
    )
    logout_user()
    return redirect(url_for('index'))


@app.route('/pop')
@login_required
def pop():
    hriks(
        'Notification: Chat Box closed.'
    )
    session.pop('room', '')
    return redirect(url_for('dashboard'))
