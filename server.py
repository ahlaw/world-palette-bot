import flask
import os

app = flask.Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

app.run(host='0.0.0.0', port=os.environ.get('PORT'))
