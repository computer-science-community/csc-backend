""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
from flask import jsonify

from flask_sqlalchemy import SQLAlchemy
import models

project_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "sqlite:///{}".format(
    os.path.join(project_dir, "eventsdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def home():
    """ more words """
    return "My flask app"


@app.route("/modify-event", methods=["GET", "POST"])
def modify_page():
    """ loads modify page with all existing events in dropdown """
    option_list = models.Event.query.all()
    return render_template("modify-event.html", option_list=option_list)


@app.route("/gather_event_info", methods=["GET", "POST"])
def gather_info():
    if request.method == 'POST':
        event_id = request.values.get('event_id')
        e_obj = db.session.query(models.Event).filter_by(id=event_id).first()
        pillar_info = db.session.query(
            models.Pillar).filter_by(id=e_obj.pillar).first()
        if pillar_info is None:
            pillar_name = ""
        else:
            pillar_name = pillar_info.name
        return jsonify([e_obj.id, pillar_name, e_obj.name, e_obj.date, e_obj.description, e_obj.link])


@app.route("/event-form", methods=["GET", "POST"])
def event_form():
    """
    this end point creates, modifies, and deltetes an event
    """
    if request.method == 'POST':
        name = request.form.get('name')
        pillar_name = request.form.get('pillar')
        date = request.form.get('date')
        description = request.form.get('description')
        link = request.form.get('link')
        delete = request.form.get('delete')
        event_id = request.values.get('event_id')
        option_list = models.Event.query.all()

        pillar = db.session.query(models.Pillar).filter_by(
            name=pillar_name).first()

        # create new event
        if event_id is None or event_id == "":
            if name is None or name == "":
                return render_template("/modify-event.html", option_list=option_list, error="Please enter an event name")
            elif date is None or date == "":
                return render_template("/modify-event.html", option_list=option_list, error="Please enter a date")
            elif (pillar_name != "") and pillar is None:
                return render_template("/modify-event.html", option_list=option_list, error="Please enter a valid Pillar name")

            pillar_id = pillar.id if pillar != None else None
            date_object = datetime.strptime(date, '%Y-%m-%dT%H:%M')

            event_object = models.Event(name=name, pillar=pillar_id,
                                        date=date_object, description=description, link=link)
            db.session.add(event_object)
            db.session.commit()
            # all_the_events = db.session.query(models.Event).all()

            return render_template("/modify-event.html", option_list=models.Event.query.all(), error="Event Created")
        # modify or delete event
        else:
            if delete:
                db.session.query(models.Event).filter_by(id=event_id).delete()
                db.session.commit()
                return render_template("/modify-event.html", option_list=models.Event.query.all(),  error="Event Deleted")
            else:

                # pillar check:
                pillar = db.session.query(models.Pillar).filter_by(
                    name=pillar_name).first()
                if (pillar_name != "") and pillar is None:
                    return render_template("/modify-event.html", option_list=option_list, error="Please enter a valid Pillar name")
                pillar_id = pillar.id if pillar != None else None

                date_object = datetime.strptime(date, '%Y-%m-%dT%H:%M')
                e_obj = db.session.query(
                    models.Event).filter_by(id=event_id).first()
                e_obj.name = name
                e_obj.pillar = pillar_id
                e_obj.date = date_object
                e_obj.description = description
                e_obj.link = link
                db.session.commit()
                return render_template("/modify-event.html", option_list=models.Event.query.all(), error="Event Updated")

        return render_template("/modify-event.html", option_list=models.Event.query.all(), error="Unknown Error")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
