from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.models import User
from flask_login import login_user, current_user, logout_user,login_required


Main = Blueprint('Main',__name__)


@Main.route('/')
def index():
    error=None  
    return render_template('main.html',error=error) 




@Main.errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404

@Main.route('/404')
def error():
    return render_template('main/404.html')