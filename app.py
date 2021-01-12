""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
import models

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
        name = request.form.get('name')
        pillar_name = request.form.get('pillar')
        date = request.form.get('date')
        description = request.form.get('description')
        link = request.form.get('link')

        pillar = db.session.query(models.Pillar).filter_by(
            name=pillar_name).first()

        if name is None or name == "":
            return render_template("/create-event.html", error="Please enter an event name")
        elif date is None or date == "":
            return render_template("/create-event.html", error="Please enter a date")
        elif (pillar_name is not None or pillar_name != "") and pillar is None:
            return render_template("/create-event.html", error="Please enter a valid Pillar name")

        pillar_id = pillar.id if pillar != None else None
        date_object = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        event_object = models.Event(name=name, pillar=pillar_id,
                                    date=date_object, description=description, link=link)
        db.session.add(event_object)
        db.session.commit()
        all_the_events = db.session.query(models.Event).all()

    return render_template("/create-event.html", error="Event Created")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
