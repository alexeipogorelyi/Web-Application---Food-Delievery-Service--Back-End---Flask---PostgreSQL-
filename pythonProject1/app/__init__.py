from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

def push_basic_data(db):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    eatings = ['first', 'second', 'third', 'fourth', 'fifth']
    for t in days:
        db.session.add(Day(idDay=t))
        db.session.commit()
    for c in eatings:
        db.session.add(Eating(idEat=c))
        db.session.commit()

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ghbdtn123@localhost/New'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app.models import Day, Eating
#push_basic_data(db)

db.create_all()








