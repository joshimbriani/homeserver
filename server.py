from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from routes.coasters.waitTime import waittime
from routes.coasters.screamscape import screamscape
from routes.coasters.goals import coastergoals
from routes.coasters.articles import articles
from database import db
from utilities.constants import UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.register_blueprint(waittime, url_prefix='/api/v1/waittime')
app.register_blueprint(screamscape, url_prefix='/api/v1/screamscape')
app.register_blueprint(coastergoals, url_prefix='/api/v1/coastergoals')
app.register_blueprint(articles, url_prefix='/api/v1/coasters/articles')

db.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route("/", defaults={'u_path': ''})
@app.route('/<path:u_path>')
def hello(u_path):
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4004), debug=True)