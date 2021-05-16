from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed

class DeleteForm(FlaskForm):
    email = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired(),Length(min=8,max=16,message='Hasło musi mieć od 8 do 16 znaków oraz składać się  z dużych liter i cyfr')])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(),EqualTo('password','Hasło się nie zgadza ')])
    submit = SubmitField('Usuń użytkownika')

class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')
