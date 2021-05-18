from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User, Note
from neuro.Account.forms import DeleteForm, UpdateForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text

Account = Blueprint('Account',__name__)

####### Main account page #######
@Account.route("/panel",methods=['GET','POST'])
@login_required
def account():
    id = current_user.id
    note = db.engine.execute(text("SELECT id,text FROM note WHERE user_id = :id ORDER BY id DESC LIMIT 1").execution_options(autocommit=True),{'id': current_user.id})
    for notes in note:
        print(notes)
    if len(notes) == 0:
        return render_template('panel.html')
    return render_template('panel.html',note=notes[1], note_id=notes[0])



@Account.route("/editUser",methods=['GET','POST'])
@login_required
def editUser():
    form = UpdateForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    

    return render_template('edit_user.html',form=form)





