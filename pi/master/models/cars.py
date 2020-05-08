from master import db

class CarModel(db.Model):
    __tablename__ = 'Cars'

    car_number = db.Column(db.String(6), primary_key=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    # default: locked = True, unlock = False
    lock_status = db.Column(db.Boolean, nullable=False, default=True)
    available = db.Column(db.Boolean, nullable=False, default= True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
