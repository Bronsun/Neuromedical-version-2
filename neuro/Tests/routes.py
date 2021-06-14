from flask import render_template, url_for, flash, redirect,request,Blueprint,json
from neuro import app,db,bcrypt
from neuro.models import User, Day, UserDay, DayText
from neuro.Tests.forms import AnswerForm
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy import text
import re

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
    mathSql = db.engine.execute(text("SELECT text FROM math WHERE day_id = :id ").execution_options(autocommit=True),{'id': day_id})
    maths = [list(row) for row in mathSql]
    correct = DayText.query.filter_by(day_id=day_id).all()
    correct_words =[]
    for corrects in correct:
        correct_words.append(corrects.text)
    
    if form.validate_on_submit():
        data = form.answer.data.upper()
        words = re.findall(r"[\w']+",data)
        a = set(words)
        b = set(correct_words)
        score = len(a&b)
        
        answer = UserDay(text=data, score=score, user_id=current_user.id, day_id=day_id)
        db.session.add(answer)
        db.session.commit()
        message = "Odpowiedź została wysłana!"
    return render_template('tests/day.html', day=day,message=message,form=form,dayTexts=json.dumps(dayTexts,ensure_ascii=False),maths=json.dumps(maths,ensure_ascii=False))


@Tests.route("/tests/numbers",methods=['GET','POST'])
@login_required
def numbers():
    return render_template('tests/numbers.html')


@Tests.route("/tests/memory",methods=['GET','POST'])
@login_required
def memory():
    return render_template('tests/memory.html')


