from flask import Flask
import os
from homeserver.web.routes.waitTime import waittime

app = Flask(__name__)
app._static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
app.register_blueprint(waittime, url_prefix='/api/waittime')

@app.route("/", defaults={'u_path': ''})
@app.route('/<path:u_path>')
def hello(u_path):
    return app.send_static_file('index.html')