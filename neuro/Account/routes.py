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
    note = db.engine.execute(text("SELECT id,text FROM note WHERE user_id = :id ORDER BY id DESC LIMIT 1").execution_options(autocommit=True),{'id': current_user.id})
    user = User.query.filter_by(id = current_user.id).first()
    notes = []
    for notes in note:
        lol ="xd"
    if len(notes) == 0:
        return render_template('panel/panel.html',note="Brak notatek", note_id=0)
    return render_template('panel/panel.html',note=notes[1], note_id=notes[0],user=user)



@Account.route("/edit",methods=['GET','POST'])
@login_required
def editUser():
    form = UpdateForm()
    user = User.query.filter_by(id=current_user.id).first()
    message = None
    if request.method == "POST":
        if form.validate_on_submit:
            user = User.query.filter_by(id=current_user.id).update(dict(name=form.name.data,phone=form.phone.data,email=form.email.data))
            db.session.commit()
            message="Dane zostały zaktualizowane"
    return render_template('panel/edit_user.html',form=form,user=user,message=message)





