from sqlalchemy.orm import relationship
from homeserver.database import db
from homeserver.models.coasters.note import CoasterGoalNote
from homeserver.models.coasters.park import CoasterPark
import json

class CoasterJournalEntry(db.Model):
    __tablename__ = 'journalentries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=False)
    content = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    park = db.Column(db.Integer, db.ForeignKey('coasterparks.id'))

    def as_dict(self):
        journal = {}
        journal["id"] = self.id
        journal["title"] = self.title
        journal["content"] = self.content
        journal["datetime"] = self.datetime.isoformat()
        journal["park"] = CoasterPark.query.get(self.park).as_dict()
        
        return journal