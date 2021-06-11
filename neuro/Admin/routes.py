from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User,UserDay, Note, Day, DayText
from neuro.Admin.forms import LoginForm, RegistrationForm, WordForm, AdminForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text
from flaskext.mysql import pymysql
from functools import wraps

Admin = Blueprint('Admin',__name__)

ROWS_PER_PAGE=15

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('NewUsers.login'))

    return wrap
####### Main account page #######
@Admin.route("/admin",methods=['GET','POST'])
@login_required
@admin_required
def admin():
    users_number = User.query.filter_by(role="patient").count()
    page = request.args.get('page',1,type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page,per_page=ROWS_PER_PAGE)
    if request.method == 'POST':
        data = request.form["search"]
        search = "%{}%".format(data)
        users = User.query.filter(User.name.like(search)).paginate(page=page,per_page=ROWS_PER_PAGE)
    return render_template('admin/admin.html',users=users,users_number=users_number)

@Admin.route("/admin/user/<int:user_id>",methods=['GET','POST'])
@login_required
@admin_required
def user(user_id):
    words = request.args.get('words',1,type=int)
    memories = request.args.get('memories',1,type=int)
    numbers = request.args.get('numbers',1,type=int)
    notes = request.args.get('notes',1,type=int)

    user = User.query.filter_by(id=user_id).first()
    day = Day.query.join(UserDay, Day.id == UserDay.day_id).add_columns(Day.number,UserDay.text,UserDay.user_id,UserDay.created_at).filter(UserDay.user_id==user_id).paginate(page=words,per_page=ROWS_PER_PAGE)
    note = Note.query.filter(Note.user_id==user_id).paginate(page=notes,per_page=3)
    return render_template('admin/admin_user.html',day=day,page_number=user_id,user=user,note=note)

@Admin.route("/admin/add",methods=['GET','POST'])
@login_required
@admin_required
def addAdmin():
    form = RegistrationForm()
    message=None
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,phone=form.phone.data, email=form.email.data, password=hashed_password,confirmed=True, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        message="Pomyślne dodano admina"
    return render_template('admin/add_admin.html',form=form,message=message)

@Admin.route("/admin/edit",methods=['GET','POST'])
@login_required
@admin_required
def editAdmin():
    form = AdminForm()
    message=None
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            duper = User.query.filter_by(id=current_user.id).update(dict(name=form.name.data))
            db.session.commit()
            message="Pomyślne zaktualizowano dane"
    return render_template('admin/edit_admin.html',message=message,user=user,form=form)

@Admin.route("/admin/test", methods=['GET','POST'])
@login_required
@admin_required
def adminTest():
    day = Day.query.all()
    return render_template('admin/admin_test.html',day=day)



@Admin.route("/admin/test/words/<int:day_id>", methods=['GET','POST'])
@login_required
@admin_required
def editTest(day_id):
    form = WordForm()
    word = DayText.query.filter_by(day_id=day_id).all()
    message=None
    if request.method == 'POST':
        for words in word:
            data = request.form[str(words.id)]
            dayTexts = DayText.query.filter_by(id=words.id).update(dict(text=data))
            db.session.commit()
            message="Pomyślne zaktualizowano dzień"
    return render_template('admin/admin_words.html',word=word,form=form,day_id=day_id,message=message)

@Admin.route("/admin/add/words/<int:day_id>", methods=['GET','POST'])
@login_required
@admin_required
def addWords(day_id):
    word = DayText(text="Edytuj słowo",day_id=day_id)
    db.session.add(word)
    db.session.commit()
    return redirect(url_for("Admin.editTest",day_id=day_id))

@Admin.route("/admin/add/words/<int:day_id>/<int:word_id>/delete", methods=['GET','POST'])
@login_required
@admin_required
def deleteWords(day_id,word_id):
    word = DayText.query.filter_by(id=word_id).first()
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for("Admin.editTest",day_id=day_id))
