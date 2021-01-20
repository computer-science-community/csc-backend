""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime
from flask import jsonify

from urllib.parse import urlparse, urljoin
from flask_sqlalchemy import SQLAlchemy
import hashlib
import models

project_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "sqlite:///{}".format(
    os.path.join(project_dir, "eventsdatabase.db"))

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
@app.route("/login")
def home():
    """ Renders login page"""
    return render_template("login.html")


@app.route("/handle-login", methods=["GET", "POST"])
def handle_login_form():
    """ Handles receiving login information """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.session.query(models.User).filter_by(
            username=username).first()

        if not user:
            return render_template("login.html", error="Invalid credentials")
        else:
            stored_password = user.password
            salt = user.salt

        new_key = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, 100000)
        if stored_password == new_key:
            login_user(user)
            next = request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)
            return render_template("modify-event.html")
        else:
            return render_template("login.html", error="Invalid credentials")
        return username + password

    else:
        return "Method Not Allowed"


@login_manager.user_loader
def load_user(user_id):
    """ Required for flask-login """
    return db.session.query(models.User).filter_by(id=int(user_id)).first()


def is_safe_url(target):
    """ Makes sure users aren't doing evil things """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@app.route("/logout")
@login_required
def logout():
    """ Log out a user and crear their cookies """
    logout_user()
    return redirect("/")


@app.route("/modify-event", methods=["GET", "POST"])
@login_required
def modify_page():
    """ loads modify page with all existing events in dropdown """
    option_list = models.Event.query.all()
    return render_template("modify-event.html", option_list=option_list)


@app.route("/gather_event_info", methods=["GET", "POST"])
@login_required
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
@login_required
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
    return "Method Not Allowed"


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
