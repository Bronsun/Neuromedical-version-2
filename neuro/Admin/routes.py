from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User, Note
from flask_login import login_user, current_user, logout_user,login_required

Admin = Blueprint('Admin',__name__)

####### Main account page #######
@Admin.route("/admin",methods=['GET','POST'])
@login_required
def admin():
    return render_template('admin.html')





