from master import db


class UserModel(db.Model):
    """
    Users table schema and validation rules.

    :param str username: primary key, length: 3-15
    :param str password:  length: 8-30, required.
    :param str first_name:  length: 1-30, required.
    :param str last_name:  length: 1-30, required.
    :param str email:  max length: 1-30, required.
    """

    __tablename__ = 'Users'

    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    bookings = db.relationship('BookingModel', backref='Users', lazy=True)

    def add_new_record(self):
        """
        Save session to database.
        """
        db.session.add(self)
        db.session.commit()
