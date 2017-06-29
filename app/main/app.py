from flask import render_template, redirect, url_for, flash as hriks
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,\
    login_user, login_required, logout_user, current_user
from .. import app, User, db, Group, Group_user
from forms import LoginForm, RegisterForm, GroupForm
from flask import session, request
from sqlalchemy import or_
import settings
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app.config['SECRET_KEY'] = settings.SECRET_KEY

Bootstrap(app)

# Setup mail server for sending confirmation
# Link to verify user.

app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USE_TSL'] = settings.MAIL_USE_TSL
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD

# setup mail service with app
mail = Mail(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

serializer = settings.serializer
s = URLSafeTimedSerializer(serializer)


# Flask_login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Default route to index
@app.route('/')
def index():
    if 'logged' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# Login route, This methods accepts both GET and POST
# requests, it renders login form page using GET request
# and submit form using POST request
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Shows login form

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.confirmed_email:
                if check_password_hash(user.password, form.password.data):
                    login_user(
                        user,
                        remember=form.remember.data
                    )
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
                        return redirect(url_for('index'))
                    return redirect(url_for('login'))
        hriks(
            'WARNING! Invalid Combination,\
            Please check username and password'
        )
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


# This is Signup form route, it accepts both GET and POST
# request. It renders signup form page using GET and submit
# form using POST request
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        token = s.dumps(email, salt='email-confirm')
        sender = 'care.androzdi@gmail.com'
        msg = Message(
            'Confirmation Email', sender=sender,
            recipients=[email]
        )
        link = url_for(
            'confirm_email', token=token,
            _external=True
        )
        msg.body = 'Please click on %s to confirm ' % (link)
        mail.send(msg)
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        admin = User.query.filter_by(
            username=str(new_user.username)
        ).first()
        admin.is_active = True
        db.session.commit()

        hriks(
            'Notification: Hey, hi %s you are all set, just click and chat!' % (
                new_user.username
            )
        )

        return redirect(url_for('dashboard'))
    hriks('Please Signup to view')
    return render_template('signup.html', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=7200)
        user = User.query.filter_by(email=str(email)).first()
        user.confirmed_email = True
        db.session.commit()
        hriks(
            'Congrats Your Email ID %s has been verified. Now, You can login' %(
                email
            )
        )
        return redirect(url_for('login'))

    except Exception as e:
        hriks(
            'Opps! something went wrong! may be session expired'
        )
        return redirect(url_for('login'))


# This is Dashboard route. It is the main page of Chat_api
# This servers as centre for all the actions taken.
# Shows user online/offline and Able to create a new group
# Add members to the group. Main link to all routes
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    users = User.query.order_by(User.username)
    groups = Group.query.order_by(Group.username)

    groups_list = []

    for group in groups:
        groups_list.append(group.group)

    group_set = set(groups_list)
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


# This route allow user to open Chat Box and let users
# chat with all other members using chat box
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


# This route allows to add member to the group
# this logic also filter group according the user
# already present.
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
        'Notification: Hey, You are currently adding member to group "%s"' % (
            group_name
        )
    )
    return render_template(
        'add.html',
        users=add_users,
        group_name=group_name,
    )


# This user allows to add new member to the group
# Group Name will be picked automatically when
# clicked on group name
@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    groups = Group.query.order_by(Group.group)

    if request.method == 'POST':
        group_name = str(request.form['group'])
        member = str(request.form['submit'])

        print member, group_name

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
            'Notification: Hey, You had just added "%s" to "%s"' % (
                member,
                group_name
            )
        )
        return redirect(url_for('dashboard'))

    return redirect(url_for('dashboard'))


# this route allows to open a new private
# chat box with user clicked to chat with.
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
        session['userd'] = 'No'
        for user in groups_users:
            if (
                str(user.user1) == str(
                    current_user.username) and str(
                    user.user2) == room) or (str(
                    user.user1) == room and str(user.user2) == str(
                    current_user.username)
            ):
                session['userd'] = 'YES'
                session['room'] = str(user.id)
                break
            else:
                session['userd'] = 'No'
        if 'userd' in session:
            if session['userd'] == 'No':
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


# This method allows to create a new group
# currently only person can be added at a time
# TODO : able to add multiple user at a time
@app.route('/group_chat', methods=['GET', 'POST'])
@login_required
def group_chat():
    form = GroupForm()
    users = User.query.order_by(User.username)

    if form.validate_on_submit():
    # validate form on submit
        if request.method == 'POST':
            name = str(current_user.username)
            group_name = str(request.form['groupname'])
            member = str(request.form['submit'])
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

            hriks(
                'Notification: You created a group with group name "%s" and added "%s" as member' % ( # noqa
                    group_name,
                    member
                )
            )
            return redirect(url_for('dashboard'))
    return render_template(
        'group.html',
        form=form,
        session=session,
        users=users
    )


# This route logout the user showing a message.
# and redirect to index page
@app.route('/logout')
@login_required
def logout():
    user = User.query.filter_by(username=str(current_user.username)).first()

    user.is_active = False
    db.session.commit()
    session.clear()
    # Clear's chatBox session,
    # this closes the chatBOX

    hriks(
        'Notification: %s Successfully Logged out' % (
            current_user.username
        )
    )

    logout_user()
    # logout_user() is called which will
    # Logout user 
    return redirect(url_for('index'))


# When ever this method is chat box will be closed
# and token for the group/user chatting will be
# dropped.
@app.route('/pop')
@login_required
def pop():
    hriks(
        'Notification: Chat Box closed.'
    )

    session.pop('room', '')
    # Clears the room and display's
    # closes chatbox, redirects to dashboard
    return redirect(url_for('dashboard'))
