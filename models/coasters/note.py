from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
import datetime

class CoasterGoalNote(Base):
    __tablename__ = 'coastergoalnotes'
    id = Column(Integer, primary_key=True)
    goal = Column(Integer, ForeignKey('coastergoals.id'))
    contents = Column(String(2000), unique=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}