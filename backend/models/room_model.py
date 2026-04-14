import uuid
from sqlalchemy import Enum

from services.data_service import db

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.String(36), 
                   primary_key=True, 
                   default=lambda: str(uuid.uuid4()))
    
    type = db.Column(Enum('direct', 'group', name='room_type'), 
                     nullable=False)

    name = db.Column(db.String(80),
                     nullable=True)