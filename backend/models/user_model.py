import uuid

from services.data_service import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), 
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    
    username = db.Column(db.String(80))
    
    password = db.Column(db.String(200))