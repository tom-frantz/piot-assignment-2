from master import db


class CarModel(db.Model):
    __tablename__ = 'Cars'

    car_number = db.Column(db.String(6), primary_key=True)
    seats = db.Column(db.Integer, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
