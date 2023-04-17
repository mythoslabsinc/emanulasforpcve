#Documentation: 12th Jan 2023
'''
This file provides api for :
    Inserting into Database
    Removing from Database
    Updating into Database
'''

#####################################################
## Imports and Variables
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_remembered, login_required
from api.Variables import *
from api.Mail import *
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import array

# ENGINE = SQLAlchemy.metadata.create_engine('sqlite:///database.sqlite', echo = True)
# SQLAlchemy.metadata.create_all(ENGINE)
db = SQLAlchemy()

# Create a class for each table inside the database
class Users(UserMixin, db.Model):
    # This class models the Profile of each User
    # primary keys are unique identifiers of data
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(100),unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lessonCount = db.Column(db.Integer, nullable=False)
    
class EmailVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), nullable=False)
    addtime = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow,onupdate=datetime.utcnow)

# User
def addUser(name, email, password):
    email = email.lower()
    newUser = Users(
        name=name,
        email=email,
        password=password,
        lessonCount=1
    )
    db.session.add(newUser)
    db.session.commit()
    return True

def increaseLessonCount(id, val):
    user = Users.query.filter_by(id=int(id)).first()
    if user.lessonCount % val != 0:
        user.lessonCount *= val
    db.session.commit()
    return True

def updateUser(id,name,password):
    User = Users.query.filter_by(id=int(id)).first()
    Users.name=name
    Users.password = password
    db.session.commit()
    return True


def updateUserPassword(email,password):
    User = getUserByEmail(email)
    User.password = password
    db.session.commit()
    return True

def getUserById(id):
    return Users.query.filter_by(id=int(id)).first()

def getUserByEmail(email):
    return Users.query.filter_by(email=email).first()

def getAllUser():
    return Users.query.all()

def getYearFilteredUser(year):
    return Users.query.filter_by(passing_year=year)

def deleteUserById(id):
    User = Users.query.filter_by(id=int(id)).first()
    if User == None: return
    db.session.delete(User)
    db.session.commit()

def deleteUserByEmail(email):
    email = email.lower()
    User = Users.query.filter_by(email=email).first()
    if User == None: return
    db.session.delete(User)
    db.session.commit()

# Email Verification
def clearVerificationCode():
    EmailVerification.query.filter(EmailVerification.addtime < datetime.utcnow()-timedelta(minutes=5)).delete()
    db.session.commit()

def addVerificationCode(email, code):
    email = email.lower()
    emailData = EmailVerification.query.filter_by(email = email).first()
    if emailData == None:
        emailData = EmailVerification(email=email,code=code)
        db.session.add(emailData)
        db.session.commit()
        db.session.refresh(emailData)
    else:
        emailData.code = code
        db.session.commit()
    clearVerificationCode()
    return True

def getVerificationCode(email):
    emailData = EmailVerification.query.filter_by(email = email).first()
    if emailData == None:
        return None
    return emailData.code