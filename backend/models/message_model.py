import uuid
from sqlalchemy import Enum

from services.data_service import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(36), 
                   primary_key=True, 
                   default=lambda: str(uuid.uuid4()))

    room_id = db.Column(db.String(36), 
                        db.ForeignKey('rooms.id', 
                        ondelete='CASCADE'), 
                        nullable=False)
    
    sender_id = db.Column(db.String(36), 
                          db.ForeignKey('users.id', 
                          ondelete='CASCADE'), 
                          nullable=False)
    
    type = db.Column(Enum('text', 'file', name='message_type'),
                     nullable=False)
    
    data = db.Column(db.JSON,
                     nullable=False)
    
    size = db.Column(db.Integer,
                     nullable=True)
    
    timestamp = db.Column(db.DateTime(timezone=True),
                          server_default=db.func.now(),
                          nullable=False)