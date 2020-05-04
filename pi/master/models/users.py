from master import db

class UserModel(db.Model):
    __tablename__ = 'Users'

    username = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(260), nullable = False)
    #email = db.Column(db.String(45), nullable = False)

    def add_new_record(self):
        db.session.add(self)
        db.session.commit()