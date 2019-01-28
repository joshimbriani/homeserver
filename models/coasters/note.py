from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from homeserver.database import db
import datetime

class CoasterGoalNote(db.Model):
    __tablename__ = 'coastergoalnotes'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Integer, db.ForeignKey('coastergoals.id'))
    contents = db.Column(db.String(2000), unique=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}