from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError

from neuro.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(min=4,max=60)])
    phone = StringField('Telefon', validators=[Length(min=9)])
    name = StringField('Imię i nazwisko', validators=[DataRequired(),Length(max=20)])
    password = PasswordField('Hasło', validators=[DataRequired(),Length(min=8,max=16,message='Hasło musi mieć przynajmniej: 8 znaków, 1 duza literę i przynajmniej 1 jedną literę')])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(),EqualTo('password','Hasła się nie zgadzają')])
    submit = SubmitField('Dodaj')
    

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).all()
       
        if user:
            raise ValidationError('Uzytkownik istnieje')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')
    remember = BooleanField('Zapamiętaj mnie')

class WordForm(FlaskForm):
    text = StringField('Słowo',validators=[DataRequired()])
    submit = SubmitField('Zapisz')