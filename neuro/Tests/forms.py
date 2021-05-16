from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed

class AnswerForm(FlaskForm):
    answer = TextAreaField('Odpowiedz')
    submit = SubmitField('Wyślij odpowiedź')