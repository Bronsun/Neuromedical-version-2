from flask import render_template, url_for, flash, redirect,request,Blueprint
from neuro import app,db,bcrypt
from neuro.NewUsers.forms import LoginForm, RegistrationForm
from neuro.models import User
from flask_login import login_user, current_user, logout_user,login_required
from neuro.NewUsers.utils import generate_confirmation_token, confirm_token,send_email
import datetime
NewUsers=Blueprint('NewUsers',__name__)


###### Login Page ##### 
@NewUsers.route('/login',methods=['GET','POST'])

def login():
    error=None
    if current_user.is_authenticated:
        return redirect(url_for('Main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.confirmed == True and user.role=="patient":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Account.account'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.confirmed == True and user.role=="admin":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Admin.admin'))
        else:
            error="Nieprawidłowe hasło lub email"
    return render_template('main/login.html', title='Login', form=form,error=error)


###### Register Page ######
@NewUsers.route("/register", methods=['GET', 'POST'])
def register():
    error=None
    if current_user.is_authenticated:
        return redirect(url_for('Main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.form.get('agree')!=None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data,phone=form.phone.data, email=form.email.data, password=hashed_password, role='patient')
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)          
            confirm_url = url_for('NewUsers.confirm_email', token=token, _external=True)
            html = render_template('email.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)

            login_user(user)

            flash('A confirmation email has been sent via email.', 'success')
            return redirect(url_for("NewUsers.verification"))
        else:
            error="You need to accept terms and policies"
    return render_template('main/register.html', title='Register', form=form,error=error)

@NewUsers.route("/verification", methods=['GET', 'POST'])
def verification():
    return render_template('main/verification.html',title='Verification')

@NewUsers.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('Account.account'))
    
######## LOGOUT ###########
@NewUsers.route('/logout')
def logout():
    logout_user()
    return redirect('login')
