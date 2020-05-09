from master import db


class UserModel(db.Model):
    __tablename__ = 'Users'

    # TODO relationship
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def add_new_record(self):
        db.session.add(self)
        db.session.commit()
