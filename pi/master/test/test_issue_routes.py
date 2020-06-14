import pytest
from master.models.users import UserModel
from master.models.cars import CarModel
from master.models.issues import IssueModel
import master.test.utils as utils
import datetime
import decimal

from master import app, db
from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.fixture
def client():
    app.config.from_object('master.config.TestingConfig')
    client = app.test_client()

    # Initial data
    car = CarModel(
        car_number='KK0001',
        make='Toyota',
        body_type='Sedan',
        colour='black',
        seats=5,
        latitude=-37.804663448,
        longitude=144.957996168,
        cost_per_hour=12,
        lock_status=True,
    )

    issue = IssueModel(
        car_number = "KK0001",
        description="issue 1 description",
        status=False
    )


    with app.app_context():
        db.drop_all()
        db.create_all()
        car.save_to_db()
        issue.save_to_db()

    yield client

def test_update_issue(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/issues/update'):
        token = create_access_token(identity=identity)
        res = client.put(
            '/issues/update', 
            data=dict(
                issue_id=1,
                description="New issue 1.",
                status=True
            ),
            headers={"Authorization": "Bearer {}".format(token)}
        )
        #result = utils.convert_byte_to_dict(res.data)
        #assert result['description'].startswith('New')
        #assert result['status']==True
        assert res.status_code == 200

def test_all_issues(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/issues/all'):
        token = create_access_token(identity=identity)
        res = client.get(
            '/issues/all', 
            headers={"Authorization": "Bearer {}".format(token)}
        )
        assert res.status_code == 200

def test_new_issue(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/issues/new'):
        token = create_access_token(identity=identity)
        res = client.post(
            '/issues/new', 
            data=dict(
                car_number='KK0001',
                description='New issue'
            ),
            headers={"Authorization": "Bearer {}".format(token)}
        )
        # result = utils.convert_byte_to_dict(res.data)
        
        assert res.status_code == 201