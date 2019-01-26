from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class CoasterPark(Base):
    __tablename__ = 'coasterparks'
    id = Column(Integer, primary_key=True)
    name = Column(String(500), unique=False)
    description = Column(String(1000), unique=False)
    rcdbID = Column(Integer)
    wikipediaLink = Column(String(500), unique=False)
    rides = relationship('CoasterRide')
    abbrev = Column(String(10), unique=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}