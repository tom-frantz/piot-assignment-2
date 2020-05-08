from master import db
from datetime import datetime
from master.models.cars import CarModel
from master.models.users import UserModel


class BookingModel(db.Model):
    __tablename__ = 'Bookings'

    booking_id = db.Column(db.Integer, primary_key=True,
                           default=1, nullable=False)
    car_number = db.Column(db.String(6), db.ForeignKey(
        CarModel.car_number), nullable=False)
    username = db.Column(db.String(100), db.ForeignKey(
        UserModel.username), nullable=False)
    # booking status: active=true, canceled=false
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
