from flask import Flask
import sys
import os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from flask_mail import Mail, Message
from api.Database import User, db as database
from api.Auth import login_manager,auth as auth_blueprint
from api.Pages import pages as pages_blueprint
from api.Mail import mailsender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rickandmorty'
login_manager.login_view = "auth.login"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SQLALCHEMY_DATABASE_URI = "{dbtype}://{username}:{password}@{hostname}/{databasename}".format(
    dbtype="postgresql+pg8000",
    username="mlhrsunu",
    password="LX1M41EbKrSr37fXVj2S4hikoVHlJAic",
    hostname="tiny.db.elephantsql.com",
    databasename="mlhrsunu"
)
# print(SQLALCHEMY_DATABASE_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


database.init_app(app)
login_manager.init_app(app)
mailsender.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# add blueprints
app.register_blueprint(pages_blueprint)
app.register_blueprint(auth_blueprint)

# In order to update database settings run the following in a separate python instance
# Make sure to make a backup of the database beforehand
# from __init__ import database,app
# with app.app_context():
#     database.create_all()