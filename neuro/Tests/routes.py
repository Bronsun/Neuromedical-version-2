from flask import render_template, url_for, flash, redirect,request,Blueprint,json
from neuro import app,db,bcrypt
from neuro.models import User, Day, UserDay
from neuro.Tests.forms import AnswerForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text

Tests = Blueprint('Tests',__name__)

####### Main Tests page #######
@Tests.route("/tests",methods=['GET','POST'])
@login_required
def tests():
    day = Day.query.all()
    return render_template('tests/tests.html', day=day)
    
@Tests.route("/tests/words",methods=['GET','POST'])
@login_required
def words():
    day = Day.query.all()
    return render_template('tests/words.html', day=day)

@Tests.route("/tests/words/<int:day_id>",methods=['GET','POST'])
@login_required
def day(day_id):
    day = Day.query.get_or_404(day_id)
    form = AnswerForm()
    message=None
    daytextSql = db.engine.execute(text("SELECT text FROM day_text WHERE day_id = :id ").execution_options(autocommit=True),{'id': day_id})
    dayTexts = [list(row) for row in daytextSql]
    if form.validate_on_submit():
        answer = UserDay(text=form.answer.data, user_id=current_user.id, day_id=day_id)
        db.session.add(answer)
        db.session.commit()
        message = "Odpowiedz została wysłana!"
    return render_template('tests/day.html', day=day,message=message,form=form,dayTexts=json.dumps(dayTexts,ensure_ascii=False))


@Tests.route("/tests/numbers",methods=['GET','POST'])
@login_required
def numbers():
    return render_template('tests/numbers.html')


@Tests.route("/tests/memory",methods=['GET','POST'])
@login_required
def memory():
    return render_template('tests/memory.html')


