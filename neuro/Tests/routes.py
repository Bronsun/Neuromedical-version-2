from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User, Day, UserDay
from neuro.Tests.forms import AnswerForm
from flask_login import login_user, current_user, logout_user,login_required

Tests = Blueprint('Tests',__name__)

####### Main Tests page #######
@Tests.route("/tests",methods=['GET','POST'])
@login_required
def tests():
    day = Day.query.all()
    return render_template('tests.html', day=day)
@Tests.route("/tests/words",methods=['GET','POST'])
@login_required
def wordss():
    day = Day.query.all()
    return render_template('words.html', day=day)

@Tests.route("/tests/words/<int:day_id>",methods=['GET','POST'])
@login_required
def day(day_id):
    day = Day.query.get_or_404(day_id)
    form = AnswerForm()
    message=None
    if form.validate_on_submit():
        answer = UserDay(text=form.answer.data, user_id=current_user.id, day_id=day_id)
        db.session.add(answer)
        db.session.commit()
        message = "Odpowiedz została wysłana!"
    return render_template('day.html', day=day,message=message,form=form)


@Tests.route("/tests/numbers",methods=['GET','POST'])
@login_required
def memory():
    return render_template('numbers.html')


