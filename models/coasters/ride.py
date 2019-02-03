from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from homeserver.database import db

class CoasterRide(db.Model):
    __tablename__ = 'coasterrides'
    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.Integer, ForeignKey('coasterparks.id'))
    waitTimes = db.relationship('CoasterWaitTime')
    tracks = db.relationship('CoasterTrack')
    name = db.Column(db.String(500), unique=False)
    description = db.Column(db.String(1000), unique=False)
    rcdbID = db.Column(db.Integer)
    wikipediaLink = db.Column(db.String(500), unique=False)
    ridden = db.Column(db.Boolean, default=False)
    coasterOrRide = db.Column(db.Boolean)
    status = db.Column(db.Integer)
    statusDate = db.Column(db.String(40), unique=False)
    openDate = db.Column(db.String(40), unique=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}