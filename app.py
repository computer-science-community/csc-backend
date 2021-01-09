""" proper file """
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """ more words """
    return "My flask app"


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
