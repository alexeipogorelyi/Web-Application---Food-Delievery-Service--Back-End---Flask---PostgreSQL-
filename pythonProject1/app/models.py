from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


# Пользователь
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    patronym = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    address = db.Column(db.String(128))
    checkadm = db.Column(db.Boolean, default=False)
    checkver = db.Column(db.Boolean, default=False)
    users = db.relationship('ActSub', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Подписка
class Subscription(db.Model):
    idSub = db.Column(db.Integer, primary_key=True)
    NameSub = db.Column(db.String(64), unique=True, nullable=True)
    DescSub = db.Column(db.String(128), nullable=True)
    KcalSub = db.Column(db.Integer, default=0)
    PriceSub = db.Column(db.Integer, nullable=True)
    SubsA = db.relationship('ActSub', backref='subs1', lazy='dynamic')
    SubsM = db.relationship('DishInMenu', backref='subs2', lazy='dynamic')

#Блюдо
class Dish(db.Model):
    idDish = db.Column(db.Integer, primary_key=True)
    NameDish = db.Column(db.Text, unique=True, nullable=True)
    DescDish = db.Column(db.String(128), nullable=True)
    KcalDish = db.Column(db.Integer, nullable=True)
    dishmen = db.relationship('DishInMenu', backref='dishh', lazy='dynamic')


#Акция
class Promo(db.Model):
    idPromo = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=True)
    DescPromo = db.Column(db.String(128), nullable=True)
    StartPromo = db.Column(db.Date, nullable=True)
    EndPromo = db.Column(db.Date, nullable=True)
    promos = db.relationship('ActSub', backref='promos', lazy='dynamic')


#Активация подписки
class ActSub(db.Model):
    idActSub = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    promo_id = db.Column(db.Integer, db.ForeignKey('promo.idPromo'))
    sub_id = db.Column(db.Integer, db.ForeignKey('subscription.idSub', ondelete='cascade'))
    StartAct = db.Column(db.Date, nullable=False)
    EndAct = db.Column(db.Date, nullable=False)
    PriceSub = db.Column(db.Integer, nullable=True)

class Day(db.Model):
    idDay = db.Column(db.Text, primary_key=True)
    dishmen = db.relationship('DishInMenu', backref='dayw', lazy='dynamic')

class Eating(db.Model):
    idEat = db.Column(db.Text, primary_key=True)
    dishmen = db.relationship('DishInMenu', backref='eat', lazy='dynamic')


class DishInMenu(db.Model):
    day = db.Column(db.Text, db.ForeignKey('day.idDay', ondelete='cascade'), primary_key=True)
    menuu = db.Column(db.Text, primary_key=True)
    sub = db.Column(db.Integer, db.ForeignKey('subscription.idSub', ondelete='cascade'), primary_key=True)
    eat_id = db.Column(db.Text, db.ForeignKey('eating.idEat', ondelete='cascade'), primary_key=True)
    dish = db.Column(db.Text, db.ForeignKey('dish.NameDish', ondelete='cascade'))

