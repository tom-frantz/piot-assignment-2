from master import db
from datetime import datetime


class IssueModel(db.Model):
    """
    Issues table schema and validation rules.

    :param int issue_id: primary key, 
    :param str description:  length: 1-1000, required.
    :param bool status: solved(`True`)/unsolved(`False`), required.

    """

    __tablename__ = 'Issues'

    issue_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    car_number = db.Column(
        db.String(6), db.ForeignKey('Cars.car_number'), nullable=False
    )
    description = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save_to_db(self):
        """
        Save session to database.
        """
        db.session.add(self)
        db.session.commit()
