from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base

class CoasterRide(Base):
    __tablename__ = 'coasterrides'
    id = Column(Integer, primary_key=True)
    goal = Column(Integer, ForeignKey('coasterparks.id'))
    name = Column(String(500), unique=False)
    description = Column(String(1000), unique=False)
    rcdbID = Column(Integer)
    wikipediaLink = Column(String(500), unique=False)
    ridden = Column(Boolean, default=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}