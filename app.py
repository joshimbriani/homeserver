import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from homeserver.database import db
from homeserver.routes.coasters.articles import articles
from homeserver.routes.coasters.goals import coastergoals
from homeserver.routes.coasters.screamscape import screamscape
from homeserver.routes.coasters.waitTime import waittime
from homeserver.utilities.constants import UPLOAD_FOLDER
from sqlalchemy_utils import create_database, database_exists

from homeserver.models.coasters.goals import CoasterGoal
from homeserver.models.coasters.note import CoasterGoalNote
from homeserver.models.coasters.park import CoasterPark
from homeserver.models.coasters.ride import CoasterRide

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.register_blueprint(waittime, url_prefix='/api/v1/waittime')
app.register_blueprint(screamscape, url_prefix='/api/v1/screamscape')
app.register_blueprint(coastergoals, url_prefix='/api/v1/coastergoals')
app.register_blueprint(articles, url_prefix='/api/v1/coasters/articles')

migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4004), debug=True)
