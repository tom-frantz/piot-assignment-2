import pytest
from master.models.users import UserModel
from master.models.cars import CarModel
from master.models.bookings import BookingModel
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
    booking = BookingModel(
        car_number='KK0001',
        username='user01',
        departure_time=datetime.date(2020, 6, 5),
        return_time=datetime.date(2020, 6, 12),
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        car.save_to_db()
        booking.save_to_db()
        db.session.commit()

    yield client


def test_add_new_car(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context('/cars/new'):
        token = create_access_token(identity=identity)
        res = client.post(
            "/cars/new",
            data=dict(
                car_number='KK0002',
                make='Mazda',
                body_type='Sedan',
                colour='black',
                seats=5,
                cost_per_hour="12.0",
            ),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = utils.convert_byte_to_dict(res.data)
        # print(result)
        # print("*****************")
        assert result['message'] != None


def test_get_car_detail(client):
    identity = {'username': 'user01'}
    token = ""
    car_number = "KK0001"
    route = '/cars/detail/{}'.format(car_number)
    with app.test_request_context(route):
        token = create_access_token(identity=identity)
        res = client.get(route, headers={"Authorization": "Bearer {}".format(token)})
        assert res.status_code == 200


def test_available_cars(client):
    # occupied rang: "2020-06-05/2020-06-12"
    identity = {'username': 'user01'}
    token = ""
    time_range = "2020-06-05/2020-06-12"

    with app.test_request_context("cars/available"):
        token = create_access_token(identity=identity)
        res = client.get(
            "cars/available",
            data=dict(time_range="2020-06-05/2020-06-12"),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        assert res.status_code == 200


def test_search_car_by_make(client):
    identity = {'username': 'user01'}
    token = ""
    make = "Toyota"
    route = "/cars/search?make={}".format(make)
    with app.test_request_context(route):
        token = create_access_token(identity=identity)
        res = client.get(route, headers={"Authorization": "Bearer {}".format(token)})
        assert res.status_code == 200


def test_get_all_cars(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context("/cars/all"):
        token = create_access_token(identity=identity)
        res = client.get(
            "/cars/all", headers={"Authorization": "Bearer {}".format(token)}
        )
        assert res.status_code == 200
