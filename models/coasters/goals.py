from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base
from models.coasters.note import CoasterGoalNote

class CoasterGoal(Base):
    __tablename__ = 'coastergoals'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), unique=False)
    description = Column(String(1000), unique=False)
    progress = Column(Integer)
    notes = relationship('CoasterGoalNote')

    # 1 = ongoing, 2 = abandoned, 3 = completed
    status = Column(Integer)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}