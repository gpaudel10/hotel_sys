#app/booking/models.py
from app import db
from datetime import datetime, timezone

class Room(db.Model):
    
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False, index=True)
    room_type = db.Column(db.String(20), nullable=False)  # given types are single, double and suite
    price_per_night = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    
    bookings = db.relationship('Booking', backref='room', lazy=True)

    def __repr__(self):
        return f'<room {self.room_number} ({self.room_type})>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='confirmed')  # given is confirmed, cancelled

    def calculate_total_price(self):
        if not self.check_in_date or not self.check_out_date or not self.room:
            return 0
        nights = (self.check_out_date - self.check_in_date).days
        if nights <= 0:
            return 0
        return self.room.price_per_night * nights

    def __repr__(self):
        return f'<booking {self.id}: room {self.room_id} ({self.check_in_date} - {self.check_out_date})>'