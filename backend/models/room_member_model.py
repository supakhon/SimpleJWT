from services.data_service import db

class RoomMember(db.Model):
    __tablename__ = 'room_members'

    room_id = db.Column(db.String(36),
                         db.ForeignKey('rooms.id', 
                         ondelete='CASCADE'),
                         primary_key=True,
                         nullable=False)
    
    user_id = db.Column(db.String(36),
                         db.ForeignKey('users.id', 
                         ondelete='CASCADE'),
                         primary_key=True,
                         nullable=False)