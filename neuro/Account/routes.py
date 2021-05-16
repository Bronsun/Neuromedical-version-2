from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User
from neuro.Account.forms import DeleteForm, UpdateForm
from flask_login import login_user, current_user, logout_user,login_required

Account = Blueprint('Account',__name__)

####### Main account page #######
@Account.route("/panel",methods=['GET','POST'])
@login_required
def account():
    
    return render_template('panel.html')



@Account.route("/editUser",methods=['GET','POST'])
@login_required
def editUser():
    form = UpdateForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    

    return render_template('edit_user.html',form=form)





