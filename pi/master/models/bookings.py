from master import db
from datetime import datetime
from master.models.cars import CarModel
from master.models.users import UserModel


class BookingModel(db.Model):
    """
    Bookings table schema and validation rules.

    :param int booking_id: primary key, auto-increment
    :param str car_number: foreign key, required.
    :param str username: foreign key, required.
    :param datetime departure_time: required.
    :param datetime return_time: required.
    """

    __tablename__ = 'Bookings'

    booking_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    car_number = db.Column(
        db.String(6), db.ForeignKey('Cars.car_number'), nullable=False
    )
    username = db.Column(
        db.String(100), db.ForeignKey('Users.username'), nullable=False
    )
    departure_time = db.Column(db.DateTime, nullable=False)
    return_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        """
        Save session to database.
        """
        db.session.add(self)
        db.session.commit()
