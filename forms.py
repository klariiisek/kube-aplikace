from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class ContactForm(FlaskForm):
    name = StringField('Jméno', validators=[
        DataRequired(message='Jméno je povinné'),
        Length(min=2, max=50, message='Jméno musí mít 2-50 znaků')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email je povinný'),
        Email(message='Neplatný email')
    ])
    message = TextAreaField('Zpráva', validators=[
        DataRequired(message='Zpráva je povinná'),
        Length(min=10, message='Zpráva musí mít alespoň 10 znaků')
    ])
    submit = SubmitField('Odeslat')

class RegistrationForm(FlaskForm):
    username = StringField('Uživatelské jméno', validators=[
        DataRequired(message='Uživatelské jméno je povinné'),
        Length(min=3, max=64, message='Uživatelské jméno musí mít 3-64 znaků')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email je povinný'),
        Email(message='Neplatný email')
    ])
    password = PasswordField('Heslo', validators=[
        DataRequired(message='Heslo je povinné'),
        Length(min=6, message='Heslo musí mít alespoň 6 znaků')
    ])
    password2 = PasswordField('Potvrďte heslo', validators=[
        DataRequired(message='Potvrďte heslo'),
        EqualTo('password', message='Hesla se musí shodovat')
    ])
    submit = SubmitField('Registrovat')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Toto uživatelské jméno je již zabrané.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Tento email je již registrovaný.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message='Email je povinný'),
        Email(message='Neplatný email')
    ])
    password = PasswordField('Heslo', validators=[
        DataRequired(message='Heslo je povinné')
    ])
    submit = SubmitField('Přihlásit se')

class ItemForm(FlaskForm):
    name = StringField('Název položky', validators=[
        DataRequired(message='Název je povinný'),
        Length(min=3, max=100, message='Název musí mít 3-100 znaků')
    ])
    description = TextAreaField('Popis')
    price = StringField('Cena', validators=[
        DataRequired(message='Cena je povinná')
    ])
    category = StringField('Kategorie', validators=[
        DataRequired(message='Kategorie je povinná'),
        Length(max=50, message='Kategorie může mít maximálně 50 znaků')
    ])
    is_available = BooleanField('Dostupné')
    submit = SubmitField('Přidat položku')
