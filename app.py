""" proper file """
from models import *
import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "sqlite:///{}".format(
    os.path.join(project_dir, "eventsdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE

db = SQLAlchemy(app)


@app.route("/")
def home():
    """ more words """
    return "My flask app"


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
