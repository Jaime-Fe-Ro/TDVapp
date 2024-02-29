from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shares = db.Column(db.Float)
    cash = db.Column(db.Float)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # email/phone number
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    portfolios = db.relationship('Portfolios')
