from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User, Day

from flask_login import login_user, current_user, logout_user,login_required

Notes = Blueprint('Notes',__name__)

####### Main Notes page #######
@Notes.route("/tests",methods=['GET','POST'])
@login_required
def notes():
    return render_template("notes.html")
    





