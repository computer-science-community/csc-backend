""" proper file """
import os

from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime
from urllib.parse import urlparse, urljoin
from flask_sqlalchemy import SQLAlchemy
from email.message import EmailMessage
import hashlib
import models
import smtplib

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
            return render_template("create-event.html")
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


@app.route("/create-event", methods=["GET", "POST"])
@login_required
def event_page():
    """ Renders page to create an event """
    return render_template("create-event.html")


@app.route('/create-event-form', methods=["POST"])
@login_required
def handle_create_event_form():
    """
    This endpoint is accessed from the create-event page.
    This page sends the data using a form.
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
    return "Method Not Allowed"


@app.route('/handle-email', methods=["POST"])
def handle_contact_us_form():
    if request.method == 'POST':
        from_email = request.form.get('emailfrom')
        email_to = request.form.get('emailto')
        subject = request.form.get('emailsubject')
        body = request.form.get('emailbody')

        if not (from_email and email_to and subject and body):
            return "All fields are required"

        email = EmailMessage()
        email['Subject'] = subject
        email['From'] = from_email
        email['To'] = email_to

        # TODO: Change this to use RIT's SMTP server. Need account and authentication
        with smtplib.SMTP('localhost') as s:
            s.send_message(email)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
