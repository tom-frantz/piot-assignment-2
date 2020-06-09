import pytest
from master.models.users import UserModel
from master.models.cars import CarModel
from master.models.bookings import BookingModel
import master.test.utils as utils
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from master import app, db
from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.fixture
def client():
    app.config.from_object('master.config.TestingConfig')
    client = app.test_client()

    # Initial data
    user = UserModel(
        username='user01',
        password=sha256.hash('password01'),
        first_name='Apple',
        last_name='Chan',
        email='user01@email.com',
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        user.add_new_record()
        db.session.commit()

    yield client


def test_api_root(client):
    res = client.get("/")
    assert res.status_code == 200


def test_register_user_valid(client):
    res = client.post(
        "/users/register",
        data=dict(
            username='user02',
            password='password02',
            first_name='Banana',
            last_name='Lin',
            email='user02@email.com',
        ),
    )
    assert res.status_code == 201


def test_register_user_invalid(client):
    res = client.post(
        "/users/register", data=dict(username='01', password='aa', email='user02')
    )
    result = utils.convert_byte_to_dict(res.data)
    result = result['message']
    assert result['username'].startswith('Value does not match')
    assert result['password'].startswith('Value does not match')
    assert result['first_name'].startswith('Missing required parameter')
    assert result['last_name'].startswith('Missing required parameter')
    assert result['email'].startswith('Value does not match')
    assert res.status_code == 400


def test_user_profile(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context('/users/me'):
        token = create_access_token(identity=identity)
        res = client.get(
            '/users/me', headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['username'] == 'user01'
        assert res.status_code == 200


def test_new_login_valid(client):
    res = client.post('/auth/new', data=dict(username='user01', password='password01'))
    result = utils.convert_byte_to_dict(res.data)
    assert result['access_token'] != None
    assert res.status_code == 201


def test_new_login_invalid(client):
    res = client.post(
        '/auth/new', data=dict(username='user01', password='passhkjhjjjklj')
    )
    assert res.status_code == 401


def test_token_refresh(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context('/auth/refresh'):
        token = create_refresh_token(identity=identity)
        res = client.post(
            '/auth/refresh', headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['access_token'] != None
        assert res.status_code == 201
