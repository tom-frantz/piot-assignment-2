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
        role ='admin'
    )

    user_2 = UserModel(
        username='user02',
        password=sha256.hash('password02'),
        first_name='Melon',
        last_name='Kuang',
        email='user02@email.com',
        role='user'
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        user.add_new_record()
        user_2.add_new_record()
        #db.session.commit()

    yield client


def test_api_root(client):
    res = client.get("/")
    assert res.status_code == 200


def test_register_user_valid(client):
    res = client.post(
        "/users/register",
        data=dict(
            username='user03',
            password='password03',
            first_name='Banana',
            last_name='Lin',
            email='user03@email.com',
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

############ STAFF FEATURES ##############

def test_user_list(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/users/all'):
        token = create_access_token(identity=identity)
        res = client.get(
            '/users/all', headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert len(result)==2
        assert res.status_code == 200

def test_user_list_invalid(client):
    identity = {'username': 'user02', 'role': 'user'}
    token = ""
    with app.test_request_context('/users/all'):
        token = create_access_token(identity=identity)
        res = client.get(
            '/users/all', headers={"Authorization": "Bearer {}".format(token)}
        )
        assert res.status_code == 403 #authorization failure

def test_user_update(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/users/update'):
        token = create_access_token(identity=identity)
        res = client.put(
            '/users/update',
            data=dict(
                username='user01',
                email='user01new@email.com',
            ), 
            headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['email']== 'user01new@email.com'
        assert res.status_code == 200

def test_user_list(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/users/delete'):
        token = create_access_token(identity=identity)
        res = client.delete(
            '/users/delete/user02', headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['message'].startswith('User')
        assert res.status_code == 200

def test_register_manager(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/users/admin-register'):
        token = create_access_token(identity=identity)
        res = client.post(
            '/users/admin-register', 
            data=dict(
                username='user03',
                password='password03',
                first_name='Banana',
                last_name='Lin',
                email='03@email.com',
                role='manager'
            ),
            headers={"Authorization": "Bearer {}".format(token)}
        )
        assert res.status_code == 201

def test_register_engineer(client):
    identity = {'username': 'user01', 'role': 'admin'}
    token = ""
    with app.test_request_context('/users/admin-register'):
        token = create_access_token(identity=identity)
        res = client.post(
            '/users/admin-register', 
            data=dict(
                username='user03',
                password='password03',
                first_name='Banana',
                last_name='Lin',
                email='03@email.com',
                role='engineer'
            ),
            headers={"Authorization": "Bearer {}".format(token)}
        )
        assert res.status_code == 201
    