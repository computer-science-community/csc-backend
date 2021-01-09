""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy
from models import Event, Pillar

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
        pillar = request.form.get('pillar')
        date = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')

        pillar_exists = db.session.query(Pillar).filter_by(
            name=pillar).first()  # TODO: fix error

        if name is None or name == "":
            return render_template("/create-event.html", error="Please enter an event name")
        elif date is None or date == "":
            return render_template("/create-event.html", error="Please enter a date")
        elif (pillar is not None or pillar != "") and pillar_exists is None:
            return render_template("/create-event.html", error="Please enter a valid Pillar name")

        event_id = ''  # TODO: generate an id
        pillar_id = ''  # TODO: get Pillar id

        event_object = Event(id=event_id, name=name, pillar=pillar_id,
                             date=date, description=description, link=link)
        db.session.add(event_object)
        db.session.commit()

    return render_template("/create-event", error="Event Created")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
