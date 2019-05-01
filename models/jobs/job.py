from homeserver.database import db

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    pythonFile = db.Column(db.String(53))
    description = db.Column(db.String(1000))
    cronString = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    lastRun = db.Column(db.DateTime)
    options = db.Column(db.String(1000))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}