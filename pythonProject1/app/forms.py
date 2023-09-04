from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите введённый пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Используйте другое имя')


class EditProfileForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия', validators=[DataRequired()])
    patronym = StringField('Отчество', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdmProfileForm(FlaskForm):
    checkadm = BooleanField('Являетесь администратором?')
    admpassword = PasswordField('Админ-пароль', validators=[DataRequired()])
    submit = SubmitField('Стать администратором')

class CreateDishForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    calories = StringField('Калорийность', validators=[DataRequired()])
    details = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateMenuForm(FlaskForm):
    days = []
    for i in range(7):
        dishes = []
        for j in range(5):
            dish = StringField('Блюдо', validators=[DataRequired()])
            dishes.append(dish)
        days.append(dishes)
    submit = SubmitField('Submit')


class CreateSubscription(FlaskForm):
    NameSub = StringField('Название', validators=[DataRequired()])
    DescSub = StringField('Описание', validators=[DataRequired()])
    PriceSub = StringField('Цена', validators=[DataRequired()])
    submit = SubmitField('Submit')