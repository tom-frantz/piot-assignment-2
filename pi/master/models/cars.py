from master import db

class CarModel(db.Model):
    __tablename__ = 'Cars'

    car_number = db.Column(db.String(6), primary_key = True)
    print('a')
    seats = db.Column(db.Integer, nullable = False)
    print('b')

    def save_to_db(self):
        print('e')
        db.session.add(self)
        print('g')
        db.session.commit()