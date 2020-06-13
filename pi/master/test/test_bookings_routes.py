import pytest
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


def test_my_booked_cars(client):
    identity = {'username': 'user01'}
    token = ""
    with app.test_request_context('/bookings/me'):
        token = create_access_token(identity=identity)
        res = client.get(
            '/bookings/me', headers={"Authorization": "Bearer {}".format(token)}
        )
        result = utils.convert_byte_to_dict(res.data)
        assert len(result) != 0
        assert res.status_code == 200

def test_add_booking_valid(client):
    # booking_period format: 2013-01-01/2013-01-01
    identity = {'username': 'user01'}
    token = ""
    car_number = "KK0001"
    booking_period = "2020-06-19/2020-06-21"
    with app.test_request_context('/bookings/new'):
        token = create_access_token(identity=identity)
        res = client.post(
            '/bookings/new',
            data=dict(car_number=car_number, booking_period=booking_period),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['message'].startswith("Your booking")
        assert res.status_code == 200

def test_add_booking_invalid(client):
    # booking_period format: 2013-01-01/2013-01-01
    identity = {'username': 'user01'}
    token = ""
    car_number = "KK0001"
    booking_period = "2020-06-07/2020-06-14"
    with app.test_request_context('/bookings/new'):
        token = create_access_token(identity=identity)
        res = client.post(
            '/bookings/new',
            data=dict(car_number=car_number, booking_period=booking_period),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = utils.convert_byte_to_dict(res.data)
        assert result['message'].startswith("Car")
        assert res.status_code == 403

def test_cancel_booking(client):
    identity = {'username': 'user01'}
    token = ""
    booking_id = 1
    route = '/bookings/cancel/{}'.format(booking_id)
    with app.test_request_context(route):
        token = create_access_token(identity=identity)
        res = client.delete(route, headers={"Authorization": "Bearer {}".format(token)})
        result = utils.convert_byte_to_dict(res.data)
        assert result['message'].startswith("Your booking")
        assert res.status_code == 200