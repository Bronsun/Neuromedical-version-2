from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail



import os


app = Flask(__name__)


app.config['SECRET_KEY']='adsadsd3123kjhg32131iplksa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://db100055789:Hotspring123@mysql-madexzpc.ogicom.pl:5432/db100055789'
app.config['SECURITY_PASSWORD_SALT'] = 'adsadsd3123kjhg32131iplksassasww221211e132d'

app.config['MAIL_SERVER'] ='smtp-madexzpc.ogicom.pl'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME'] = 'info.neuromedical.madexzpc'
app.config['MAIL_PASSWORD'] = 'NeuroMateusz12!'
app.config['MAIL_DEFAULT_SENDER'] = 'info@neuromedical.pl'




db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'NewUsers.login'
mail.init_app(app)
from neuro.Account.routes import Account
from neuro.Main.routes import Main
from neuro.NewUsers.routes import NewUsers
from neuro.Tests.routes import Tests
from neuro.Notes.routes import Notes
from neuro.Admin.routes import Admin

app.register_blueprint(Admin)
app.register_blueprint(Notes)
app.register_blueprint(Tests)
app.register_blueprint(Account)
app.register_blueprint(Main)
app.register_blueprint(NewUsers)

