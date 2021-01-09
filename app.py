""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy
""" from models import Event, Pillar, User """

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


@app.route("/create-event", methods=["GET", "POST"])
def event_page():
    """ view event-page html """
    return render_template("create-event.html")


@app.route('/create-event-form', methods=["POST"])
def handle_create_event_form():
    """
    This endpoint is accessed from the create-event page.
    This page send the data using a form.
    """
    if request.method == 'POST':
        pillar = request.form.get('pillar')
        name = request.form.get('name')
        date = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')

        if name is None or name == "":
            return render_template("/create-event.html", error="Please enter an event name")
        elif date is None or date == "":
            return render_template("/create-event.html", error="Please enter a date")
    return render_template("/")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
