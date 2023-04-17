#Documentation: 12th Jan 2023
'''
This file provides api for :
    Login
    Logout
    Register
    Forgot Password
    Edit Profile
'''

#####################################################
## Imports and Variables
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from api.Variables import *
from flask import Blueprint, request, flash, redirect, url_for, render_template
import api.Database as Database
import api.Mail as Mail
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from itsdangerous import URLSafeSerializer
from datetime import datetime

# class SignForm(Form):
# 	email =StringField("Email",[validators.DataRequired("Please enter your email.")])
# 	pswd = PasswordField("Password",[validators.DataRequired("Please enter your password")])
# 	submit=SubmitField("Login")


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
secret_code_generator = URLSafeSerializer('ItsSecret!DontTellAnyone')

#####################################################
## Create an Auth Blueprint
auth = Blueprint('auth',__name__, template_folder='templates')

#####################################################
## Login and Logout
@auth.route('/login',methods=["GET",'POST'])
def login():
    # if the response didn't come
    if request.method != 'POST':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    # Find User profile corresponding to email
    userProfile = Database.getUserByEmail(email)
    #verify data
    if not userProfile:
        flash("Email not found, please sign up ")
        return redirect(url_for('auth.signup'))
    elif not check_password_hash(userProfile.password,password):
        flash("Wrong Password, recheck credentials and try again")
        return render_template('login.html')
    #login the corresponding user and redirect to corresponding Profile Page
    login_user(userProfile,remember=remember)
    return redirect(url_for('pages.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.home'))

#####################################################
## Sign Up
@auth.route('/email-verify/',methods = ['POST'])
def emailVerify():
    if request.method != 'POST':
        return redirect(url_for('.signup'))
    user_email = request.form.get('email')
    if Database.getUserByEmail(user_email):
        flash("Email Already Registered, If you have forgot password then try Forgot Password Option")
        return redirect(url_for('.signup'))
    otp = randint(000000,999999)
    Database.addVerificationCode(user_email,otp)
    Mail.sendOTP(user_email,otp)
    return redirect(url_for(".signup",step="otp-verify", email = user_email))

@auth.route('/otp-verify/',methods=['POST'])
def otpVerify():
    if request.method != 'POST':
        return redirect(url_for('.signup'))
    user_email = request.form.get('email')
    user_otp = request.form.get('otp')
    otp = Database.getVerificationCode(user_email)
    if otp == None or str(otp) != str(user_otp):
        flash("Invalid OTP")
        return redirect(url_for(".signup"))
    else:
        return redirect(url_for('.signup',step='register', email= user_email, code=secret_code_generator.dumps(user_email)))

@auth.route("/signup/")
@auth.route("/signup" + '/<step>&<email>/')
@auth.route("/signup" + '/<step>&<email>&<code>/')
def signup(step = 'email-verify',email='null',code='null'):
    parameters={
        'step' : step,
        'email' : email,
        'code' : code,
    }
    return render_template('signup.html',parameters = parameters)

@auth.route('/register/<code>',methods=['POST'])
def register(code):
     # for storing data step
    if request.method != 'POST':
        flash("Unauthorized")
        return redirect(url_for(".signup"))
    else:
        email = request.form.get('email')
        password = request.form.get('pswd1').strip()
        password2 = request.form.get('pswd2').strip()
        # print("*"+password+"*")
        # print("*"+password2+"*")
        name = request.form.get('name')
        # Code check
        if secret_code_generator.dumps(email) != code:
            flash("Invalid URL")
            return redirect(url_for(".signup"))
        # Password Check
        if ( password != password2 ):
            flash('Please enter your password properly')
            return redirect(url_for('.signup',step='register', email= email, code=code))
        # email check
        if type(Database.getUserByEmail(email)) != type(None):
            flash("Can't use this email, Email already taken")
            return redirect(url_for('.signup',step='register', email= email, code=code))
        # store all the data
        hash = generate_password_hash(password, method='sha256')
        # print(password, hash, check_password_hash(hash,password))
        Database.addUser(name.capitalize(),email, hash)
        return redirect(url_for('.login'))


#####################################################
## Reset Password
@auth.route('/reset-password')
@auth.route('/reset-password/<step>', methods=['GET','POST'])
@auth.route('/reset-password/<step>&<email>', methods=['GET','POST'])
@auth.route('/reset-password/<step>&<email>&<code>', methods=['GET','POST'])
def resetPassword(step = '',email='null',code='null'):
    parameters={
        'step' : step,
        'email' : email,
        'code' : code,
    }
    if step == 'email-verify' :
        if request.method != 'POST':
            return render_template('forgotPswd.html',parameters = parameters)
        email = request.form.get('email')
        if Database.getUserByEmail(email):
            otp = randint(000000,999999)
            Database.addVerificationCode(email,otp)
            Mail.sendOTP(email,otp)
            return redirect(url_for(".resetPassword",step="otp-verify",email=email))
        else:
            flash("We can't find any account with email: "+ str(email))
            return render_template('forgotPswd.html',parameters = parameters)
    elif step == 'otp-verify':
        if request.method != 'POST':
            step = "email-verify"
            return render_template('forgotPswd.html',parameters = parameters)
        user_email = request.form.get('email')
        user_otp = request.form.get('otp')
        otp = Database.getVerificationCode(user_email)
        if otp == None or str(otp) != str(user_otp):
            flash("Invalid OTP")
            return redirect(url_for(".resetPassword", step="otp-verify", email=email))
        else:
            return redirect(url_for('.resetPassword',step='password-set', email= user_email, code=secret_code_generator.dumps(user_email)))
    elif step == "password-set":
        if request.method != 'POST':
            step = "email-verify"
            return render_template('forgotPswd.html',parameters = parameters)
        else:
            email = request.form.get('email')
            password = request.form.get('pswd1')
            password2 = request.form.get('pswd2')
            # Code check
            if secret_code_generator.dumps(email) != code:
                flash("Invalid URL")
                return redirect(url_for(".resetPassword"))
            # Password Check
            if ( password != password2 ):
                flash('Please enter your password properly')
                return redirect(url_for('.resetPassword',step='register', email= email, code=code))
            # store all the data
            if not Database.updateUserPassword(email,generate_password_hash(password, method='sha256')):
                flash("Some Error Occured, Please try again")
                return redirect(url_for('.resetPassword'))
            return redirect(url_for('.login'))
    else:
        if(step != ""):
            flash(step)
        parameters['step'] = "email-verify"
        return render_template('forgotPswd.html',parameters = parameters)
        

