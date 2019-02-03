from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from homeserver.database import db

class CoasterWaitTime(db.Model):
    __tablename__ = 'coasterwaittimes'
    id = db.Column(db.Integer, primary_key=True)
    park = db.Column(db.Integer, ForeignKey('coasterparks.id'))
    ride = db.Column(db.Integer, ForeignKey('coasterrides.id'))
    waitTime = db.Column(db.Integer)
    weather = db.Column(db.String(40))
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    windspeed = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    earlyEntry = db.Column(db.Boolean)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}