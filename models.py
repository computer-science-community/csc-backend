""" words """
from app import db


class Event(db.Model):
    """ Event table definition """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    pillar = db.Column(db.Integer, db.ForeignKey('pillar.id'))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500))
    link = db.Column(db.String(300))

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class Pillar(db.Model):
    """ 
    Pillar table definition
    All tables are created by the init_database script
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<Pillar: id={}, name={}, email={}>".format(self.id, self.name, self.email)


class User(db.Model):
    """ User table definition """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True,  nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(200))

    def __repr__(self):
        return "<User: id={}, username={}, email={}>".format(self.id, self.username, self.email)

    def is_authenticated(self):
        """ Required by flask-login """
        return True

    def is_active(self):
        """ Required by flask-login """
        return True

    def is_anonymous(self):
        """ Required by flask-login """
        return False

    def get_id(self):
        """ Required by flask-login """
        return str(self.id).encode("utf-8")
