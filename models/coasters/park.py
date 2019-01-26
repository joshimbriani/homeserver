from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import db

class CoasterPark(db.Model):
    __tablename__ = 'coasterparks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=False)
    description = db.Column(db.String(1000), unique=False)
    rcdbID = db.Column(db.Integer)
    wikipediaLink = db.Column(db.String(500), unique=False)
    rides = db.relationship('CoasterRide')
    abbrev = db.Column(db.String(10), unique=False)
    #status = db.Column(db.Integer)
    #address = db.Column(db.String(100), unique=False)
    #openDate = db.Column(db.String(40), unique=False)
    #statusDate = db.Column(db.String(40), unique=False)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}