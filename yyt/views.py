from yyt import app
from flask import render_template, flash, redirect
from forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    user = {'nickname':'DanielKoo'}
    posts = [{'author':{'nickname':"DanielKoo"}, 'body':'Hello, DanielKoo'}, {'author':{'nickname':'JamesBond'}, 'body':'Very Super JamesBond'}, {'author':{'nickname':'JackyChen'}, 'body':'Awesome JackyChen'}]
    return render_template('index.html', title = 'Aloha', user = user, posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login request for OpenID %s, remember me %s' % (form.openid.data, str(form.remember_me.data)))
        return redirect('index')
    return render_template('login.html', title = 'Sign in', form = form, providers=app.config['OPENID_PROVIDERS'])


