from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User,UserDay, Note, Day, DayText,Math
from neuro.Admin.forms import LoginForm, RegistrationForm, WordForm, AdminForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text
from flaskext.mysql import pymysql
from functools import wraps
from sqlalchemy.sql import func
Admin = Blueprint('Admin',__name__)

ROWS_PER_PAGE=25

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for('Main.error'))

    return wrap
####### Main account page #######
@Admin.route("/admin",methods=['GET','POST'])
@login_required
@admin_required
def admin():
    users_number = User.query.filter_by(role="patient").count()
    page = request.args.get('page',1,type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page,per_page=ROWS_PER_PAGE)
    test_number = UserDay.query.count()
    average = db.session.query(func.avg(UserDay.score)).scalar()
    if request.method == 'POST':
        data = request.form["search"]
        search = "%{}%".format(data)
        users = User.query.filter(User.name.like(search)).paginate(page=page,per_page=ROWS_PER_PAGE)
    return render_template('admin/admin.html',users=users,users_number=users_number,test_number=test_number,average=average)

@Admin.route("/admin/user/<int:user_id>",methods=['GET','POST'])
@login_required
@admin_required
def user(user_id):
    words = request.args.get('words',1,type=int)
    memories = request.args.get('memories',1,type=int)
    numbers = request.args.get('numbers',1,type=int)
    notes = request.args.get('notes',1,type=int)

    user = User.query.filter_by(id=user_id).first()
    day = Day.query.join(UserDay, Day.id == UserDay.day_id).add_columns(Day.number,Day.id,UserDay.total,UserDay.text,UserDay.id,UserDay.score,UserDay.user_id,UserDay.created_at).filter(UserDay.user_id==user_id).paginate(page=words,per_page=10)
    if len(day.items) ==0:
        count_words = 0 
        note = Note.query.filter(Note.user_id==user.id).paginate(page=notes,per_page=3)
      
    else:
        days = [row for row in day.items[0]]
        count_words = DayText.query.filter_by(day_id=days[1]).count()    
        note = Note.query.filter(Note.user_id==user.id).paginate(page=notes,per_page=3)
    return render_template('admin/admin_user.html',day=day,page_number=user_id,user=user,note=note,count_words=count_words)

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
    math = Math.query.filter_by(day_id=day_id).all()
    message=None
    if request.method == 'POST':
        for words in word:
            data = request.form[str(words.id)]
            dayTexts = DayText.query.filter_by(id=words.id).update(dict(text=data.upper()))
            db.session.commit()
        for maths in math:
            data = request.form[str(maths.id)]
            mathematics = Math.query.filter_by(id=maths.id).update(dict(text=data.upper()))
            db.session.commit()
            message="Pomyślne zaktualizowano dzień"
    return render_template('admin/admin_words.html',word=word,math=math,form=form,day_id=day_id,message=message)

@Admin.route("/admin/add/words/<int:day_id>", methods=['GET','POST'])
@login_required
@admin_required
def addWords(day_id):
    word = DayText(text="Edytuj słowo",day_id=day_id)
    db.session.add(word)
    db.session.commit()
    return redirect(url_for("Admin.editTest",day_id=day_id))

@Admin.route("/admin/add/maths/<int:day_id>", methods=['GET','POST'])
@login_required
@admin_required
def addMath(day_id):
    math = Math(text="Edytuj zadanie",day_id=day_id)
    db.session.add(math)
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

@Admin.route("/admin/answer/<int:user_day_id>/delete", methods=['GET','POST'])
@login_required
@admin_required
def deleteAnswer(user_day_id):
    word = UserDay.query.filter_by(id=user_day_id).first()
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for("Admin.user",user_id=word.user_id))

@Admin.route("/admin/add/maths/<int:day_id>/<int:math_id>/delete", methods=['GET','POST'])
@login_required
@admin_required
def deleteMaths(day_id,math_id):
    math = Math.query.filter_by(id=math_id).first()
    db.session.delete(math)
    db.session.commit()
    return redirect(url_for("Admin.editTest",day_id=day_id))

@Admin.route("/admin/messages", methods=['GET','POST'])
@login_required
@admin_required
def messages():
    page = request.args.get('page',1,type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page,per_page=ROWS_PER_PAGE)
    return render_template('admin/messages.html',users=users)