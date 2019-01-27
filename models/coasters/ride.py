from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from homeserver.database import db

class CoasterRide(db.Model):
    __tablename__ = 'coasterrides'
    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.Integer, ForeignKey('coasterparks.id'))
    name = db.Column(db.String(500), unique=False)
    description = db.Column(db.String(1000), unique=False)
    rcdbID = db.Column(db.Integer)
    wikipediaLink = db.Column(db.String(500), unique=False)
    ridden = db.Column(db.Boolean, default=False)
    coasterOrRide = db.Column(db.Boolean)
    modelLayout = db.Column(db.String(500), unique=False)
    configuration = db.Column(db.String(500), unique=False)
    modelCategory = db.Column(db.String(500), unique=False)
    status = db.Column(db.Integer)
    make = db.Column(db.String(500), unique=False)
    statusDate = db.Column(db.String(40), unique=False)
    openDate = db.Column(db.String(40), unique=False)
    coasterType = db.Column(db.String(500), unique=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}