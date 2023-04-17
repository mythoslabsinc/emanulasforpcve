#Documentation: 11th Jan 2022
'''
This file provides api for :
    Rendering all pages
'''

#####################################################
## Imports and Variables
from datetime import datetime
import os
from flask import render_template,request,redirect,url_for
from flask import Blueprint
from flask_login import login_required, current_user
import api.Database as Database
import json
from flask import jsonify
from api.Variables import *
import api.Mail as Mail

#####################################################
## Create a Pages Blueprint
pages = Blueprint('pages',__name__, template_folder='templates')

@pages.route('/')
@pages.route('/Home/')
@pages.route('/home')
def home():
    idx = -1
    try:
        idx = current_user.lessonCount
    except:
        pass
    return render_template('index.html', topics = MODULES, idx = idx)

@pages.route('/module/<id>')
@login_required
def module(id = 0):
    id = int(id)
    code = MODULES[id][1]
    title = MODULES[id][0]
    return render_template("typeformTemplate.html",code = code, email = current_user.email, name=current_user.name, id = id, title = title)


@pages.route('/completed/<id>')
@login_required
def complete(id):
    id = int(id)
    # Mail.sendCertificate(current_user.email, current_user.name)
    Database.increaseLessonCount(current_user.id, MODULES[id][2])
    if id < len(MODULES):
        return redirect(url_for("pages.module", id = id+1))
    return redirect(url_for("pages.home"))