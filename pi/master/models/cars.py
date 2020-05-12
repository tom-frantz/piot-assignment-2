from master import db


class CarModel(db.Model):
    __tablename__ = 'Cars'

    car_number = db.Column(db.String(6), primary_key=True, nullable=False)
    make = db.Column(db.String(30), nullable=False)
    body_type = db.Column(db.String(30), nullable=False)
    colour = db.Column(db.String(30), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    # default: -37.804663448,144.957996168
    latitude = db.Column(db.Numeric(11, 9), default=-37.804663448, nullable=False)
    longitude = db.Column(db.Numeric(12, 9), default=144.957996168, nullable=False)
    cost_per_hour = db.Column(db.Numeric, nullable=False)

    # default: locked = True, unlock = False
    lock_status = db.Column(db.Boolean, nullable=False, default=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    bookings = db.relationship('BookingModel', backref='Cars', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
