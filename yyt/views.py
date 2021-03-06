from yyt import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm, EditForm
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from datetime import datetime

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = g.user
    posts = [
        {'author':{'nickname':"DanielKoo"}, 'body':'Hello, DanielKoo'},
        {'author':{'nickname':'JamesBond'}, 'body':'Very Super JamesBond'},
        {'author':{'nickname':'JackyChen'}, 'body':'Awesome JackyChen'}
    ]
    return render_template('index.html', title='Aloha', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        # flash('Login request for OpenID %s, remember me %s' % (form.openid.data, str(form.remember_me.data)))
        # return redirect('index')
    return render_template('login.html', title='Sign in', form=form, providers=app.config['OPENID_PROVIDERS'])

@app.before_request
def before_request():
    g.user = current_user #global var set by flask_login
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash('Invalid login, please login')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author':user, 'body': 'Test Post #1'},
        {'author':user, 'body': 'Test Post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('edit.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500