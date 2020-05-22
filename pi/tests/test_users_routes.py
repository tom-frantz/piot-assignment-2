import pytest
from master.models.users import UserModel
from master.models.cars import CarModel
from master.models.bookings import BookingModel
import tests.utils as utils
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from master import app, db
# import master
from flask_jwt_extended import create_access_token, create_refresh_token

@pytest.fixture
def client():
    app.config.from_object('master.config.TestingConfig')
    client = app.test_client()

    #Initial data
    user = UserModel(
        username='user01', 
        password=sha256.hash('password01'), 
        first_name='Apple', 
        last_name='Chan', 
        email='user01@email.com')
    
    car = CarModel(
        car_number = 'KK0001',
        make = 'Toyota',
        body_type = 'Sedan',
        colour = 'black',
        seats = 5,
        latitude = -37.804663448,
        longitude = 144.957996168,
        cost_per_hour = 12,
        lock_status = True
        )
    booking = BookingModel(
        car_number = 'KK0001',
        username = 'user01',
        departure_time = datetime.date(2020, 6, 5),
        return_time = datetime.date(2020, 6, 12)
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        user.add_new_record()
        car.save_to_db()
        booking.save_to_db()
        db.session.commit()
          
    yield client

# @pytest.fixture
# def app(mocker):
#     mocker.patch("flask_sqlalchemy.SQLAlchemy.drop_all", return_value=True)
#     mocker.patch("flask_sqlalchemy.SQLAlchemy.create_all", return_value=True)
#     # mocker.patch("flask_sqlalchemy.SQLAlchemy.orm.session.add", return_value=True)
#     #mocker.patch("master.models.users.UserModel.add_new_record", return_value=True)
#     mocker.patch('flask_jwt_extended.view_decorators.verify_jwt_in_request', return_value=True)
#     # mock = mocker.MagicMock(dict(username='user01', role='user'))
#     # mocker.patch("flask_jwt_extended.utils.get_jwt_identity", mock)
#     app = master.app
#     return app

def test_api_root(client):
    res = client.get("/")
    assert res.status_code == 200

def test_register_user_valid(client):
    res = client.post(
        "/users/register", data=dict(
            username = 'user02', 
            password = 'password02',
            first_name = 'Banana',
            last_name = 'Lin',
            email = 'user02@email.com'
            ))
    # result = utils.convert_byte_to_dict(res.data)
    # assert result['username'] == 'user02'
    # assert result['access_token'] != None
    # assert result['refresh_token'] != None
    assert res.status_code == 201


def test_register_user_invalid(client):
    res = client.post(
        "/users/register", data=dict(
            username = '01', 
            password = 'aa',
            email = 'user02'
            ))
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
        res = client.get('/users/me', headers = {"Authorization": "Bearer {}".format(token)})
        result = utils.convert_byte_to_dict(res.data)
        assert result['username']== 'user01'
        assert res.status_code == 200

def test_new_login_valid(client):
    res = client.post('/auth/new', data=dict(username='user01', password='password01'))
    result = utils.convert_byte_to_dict(res.data)
    assert result['access_token'] != None
    assert res.status_code == 201

def test_new_login_invalid(client):
    res = client.post('/auth/new', data=dict(username='user01', password='passhkjhjjjklj'))
    assert res.status_code == 401

def test_token_refresh(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context('/auth/refresh'):    
        token = create_refresh_token(identity=identity)
        res = client.post('/auth/refresh', headers = {"Authorization": "Bearer {}".format(token)})
        result = utils.convert_byte_to_dict(res.data)
        assert result['access_token'] != None
        assert res.status_code == 201

# def test_token_refresh_invalid(client):
#     token = "alsdjfkldjkfjdsjflkjdsfjldfkslfaj"

#     res = client.post('/auth/refresh', headers = {"Authorization": "Bearer {}".format(token)})
#     result = utils.convert_byte_to_dict(res.data)
#     print(result)
#     print(res.status_code)
    # assert result['access_token'] != None
    # assert res.status_code == 201

# def test_change_password_valid(client):
#     identity = {'username': 'user01', 'role': 'user'}
#     token = ""
#     with app.test_request_context('/auth/password'):    
#         token = create_access_token(identity=identity)
#         res = client.post(
#             '/auth/password', 
#             data=dict(old_password='password01', new_password='newpass01'),
#             headers = {"Authorization": "Bearer {}".format(token)})
#         result = utils.convert_byte_to_dict(res.data)
#         assert result['access_token'] != None
#         assert res.status_code == 201

# TODO Fix password validation
# def test_change_password_invalid(client):
#     identity = {'username': 'user01', 'role': 'user'}
#     token = ""
#     with app.test_request_context('/auth/password'):    
#         token = create_access_token(identity=identity)
#         res = client.post(
#             '/auth/password', 
#             data=dict(old_password='wrong_password', new_password='newpass01'),
#             headers = {"Authorization": "Bearer {}".format(token)})
#         result = utils.convert_byte_to_dict(res.data)
#         print(result)
#         print("************")
        #assert result['access_token'] != None
        #assert res.status_code == 201

