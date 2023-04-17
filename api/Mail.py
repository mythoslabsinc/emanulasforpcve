#Documentation: 10th Jan 2022
'''
This file provides api for :
    Sending Mail
    Sending OTP
'''

#####################################################
## Imports and Variables
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from api.Variables import *
from flask import Flask, Blueprint, request
# from api.Database import getAlumniByEmail
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from PIL import Image, ImageDraw, ImageFont
import datetime

#####################################################
## Create an Mail Blueprint
app =Flask(__name__)
mail = Blueprint('mail',__name__)
app.config['MAIL_SERVER']='smtp.gmail.com' # need to find this out w.r.t email type
app.config['MAIL_PORT'] = 465 # need to find this out w.r.t email type
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mailsender = Mail(app)


def sendOTP(email, otp):
    msg = Message('Verification of E-mail', sender = MAIL_USERNAME, recipients = [email])
    msg.body = "Hi, We recieved a request for email confirmation for this email. Your Verification Code is " + str(otp)
    # msg.html=render_template('emailtemplate.html',otp = otp)
    # msg.body would load in case msg.html fails
    mailsender.send(msg)
    
def generateCertificate(name):
    date = datetime.datetime.now().strftime("%d/%m/%y")
    certificate = HOME+"/static/images/certTemplate.png"
    text_y_position = 0.45 # in fraction
    text_x_position = 0.5
    # opens the image
    img = Image.open(certificate, mode ='r')
        
    # gets the image dimensions
    image_width = img.width
    image_height = img.height 
    
    name_font = ImageFont.truetype(HOME + "/static/font/Courgette-Regular.ttf", 90)
    date_font = ImageFont.truetype(HOME + "/static/font/Courgette-Regular.ttf", 30)
    image_editable = ImageDraw.Draw(img)
    text_width, text_height = image_editable.textsize(name)
    image_editable.text(
        (
            image_width*text_x_position - text_width/2,
            image_height*text_y_position - text_height/2
        ),
        name, font=name_font,
        fill="#000000", 
        anchor="ma", width=3)
    image_editable.text(
        (
            image_width*0.6,
            image_height*0.55
        ), 
        date, 
        font=date_font,fill="#000000", anchor="md")
    # saves the image in png format
    img.save("{}.png".format("sample")) 
    return img

def sendCertificate(email, name):
    generateCertificate(name) 
    msg = Message('Module Completion Certificate', sender = MAIL_USERNAME, recipients = [email])
    msg.body = "Congratulations on completing the module. Here is your certificate "
    # msg.attach(generateCertificate(name))
    # with generateCertificate(name) as fp:
    #     msg.attach("certificate.png", "image/png", fp.tobytes("hex", "rgb"))
    # mailsender.send(msg)