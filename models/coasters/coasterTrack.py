from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from homeserver.database import db

class CoasterTrack(db.Model):
    __tablename__ = 'coastertracks'
    id = db.Column(db.Integer, primary_key=True)
    coaster = db.Column(db.Integer, ForeignKey('coasterrides.id'))
    height = db.Column(db.Integer)
    inversions = db.Column(db.Integer)
    length = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    elements = db.Column(db.String(500), unique=False)
    duration = db.Column(db.String(10), unique=False)
    verticalAngle = db.Column(db.Integer)
    drop = db.Column(db.Integer)
    modelLayout = db.Column(db.String(500), unique=False)
    configuration = db.Column(db.String(500), unique=False)
    modelCategory = db.Column(db.String(500), unique=False)
    coasterType = db.Column(db.String(500), unique=False)
    make = db.Column(db.String(500), unique=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}