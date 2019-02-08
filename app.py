import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from homeserver.database import db
from homeserver.routes.coasters.articles import articles
from homeserver.routes.coasters.goals import coastergoals
from homeserver.routes.coasters.screamscape import screamscape
from homeserver.routes.coasters.waitTime import waittime
from homeserver.routes.coasters.tripjournal import tripjournals
from homeserver.routes.coasters.parks import parks
from homeserver.routes.jobs.job import jobs
from homeserver.utilities.constants import UPLOAD_FOLDER
from sqlalchemy_utils import create_database, database_exists

from homeserver.models.coasters.goals import CoasterGoal
from homeserver.models.coasters.note import CoasterGoalNote
from homeserver.models.coasters.park import CoasterPark
from homeserver.models.coasters.ride import CoasterRide
from homeserver.models.coasters.journalEntry import CoasterJournalEntry
from homeserver.models.coasters.waitTimes import CoasterWaitTime
from homeserver.models.coasters.coasterTrack import CoasterTrack

from homeserver.models.jobs.job import Job

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + "/data/homeserver.db"

app.register_blueprint(waittime, url_prefix='/api/v1/coasters/waittimes')
app.register_blueprint(screamscape, url_prefix='/api/v1/screamscape')
app.register_blueprint(coastergoals, url_prefix='/api/v1/coastergoals')
app.register_blueprint(articles, url_prefix='/api/v1/coasters/articles')
app.register_blueprint(tripjournals, url_prefix='/api/v1/coasters/journals')
app.register_blueprint(parks, url_prefix='/api/v1/coasters/parks')
app.register_blueprint(jobs, url_prefix='/api/v1/jobs')

migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "/data/homeserver.db"):
        print("No database found. Creating one")
        create_database(app.config['SQLALCHEMY_DATABASE_URI'], encoding='utf8mb4')
        db.create_all()
        db.session.commit()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route("/", defaults={'u_path': ''})
@app.route('/<path:u_path>')
def hello(u_path):
    return render_template('index.html')

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4004), debug=True)
