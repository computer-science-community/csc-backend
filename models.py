""" words """
from app import db


class Event(db.Model):
    """ words """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    pillar = db.Column(db.Integer, db.ForeignKey('pillar.id'))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500))
    link = db.Column(db.String(300))

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class Pillar(db.Model):
    """ pillar info """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)


class User(db.Model):
    """ user info """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True,  nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), nullable=False)
