from master import db


class CarModel(db.Model):
    """
    Cars table schema and validation rules.

    :param str car_number: primary key, max length: 6
    :param str make: max length: 30, required.
    :param str body_type: max length: 30, required.
    :param int seats: range: 1-12, required.
    :param str colour: max length: 30, required.
    :param decimal cost_per_hour: non-negative, required.
    :param decimal latitude: range: -90 to 90, required.
    :param decimal longitude: range: -180 to 180, required.
    :param bool lock_status: required.
    """

    __tablename__ = 'Cars'

    car_number = db.Column(db.String(6), primary_key=True, nullable=False)
    make = db.Column(db.String(30), nullable=False)
    body_type = db.Column(db.String(30), nullable=False)
    colour = db.Column(db.String(30), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    # default: -37.804663448,144.957996168
    latitude = db.Column(db.Numeric(11, 9), default=-37.804663448, nullable=False)
    longitude = db.Column(db.Numeric(12, 9), default=144.957996168, nullable=False)
    cost_per_hour = db.Column(db.Numeric(6, 2), nullable=False)

    # default: locked = True, unlock = False
    lock_status = db.Column(db.Boolean, nullable=False, default=True)
    bookings = db.relationship('BookingModel', backref='Cars', lazy=True)
    reported_issues = db.relationship('IssueModel', backref='Cars', lazy=True)

    def save_to_db(self):
        """
        Save session to database.
        """
        db.session.add(self)
        db.session.commit()
