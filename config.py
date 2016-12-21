# config flask-wtf
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

# config flask_sqlalchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print ">>>>basedir: %s" % basedir
print ">>>>__file__: %s" % __file__
print ">>>>os.path.dirname(__file__): %s " % os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'yytapp.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'yytdb_repository')

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['845296516@qq.com']