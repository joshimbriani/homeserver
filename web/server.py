from flask import Flask
from homeserver.web.routes.waitTime import waittime

app = Flask(__name__)
app.register_blueprint(waittime, url_prefix='/api/waittime')

@app.route("/")
def hello():
    return "Hello World!"