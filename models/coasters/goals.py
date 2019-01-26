from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import db
from models.coasters.note import CoasterGoalNote

class CoasterGoal(db.Model):
    __tablename__ = 'coastergoals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=False)
    description = db.Column(db.String(1000), unique=False)
    progress = db.Column(db.Integer)
    notes = db.relationship('CoasterGoalNote')

    # 1 = ongoing, 2 = abandoned, 3 = completed
    status = db.Column(db.Integer)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}