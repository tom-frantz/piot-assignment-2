from operation import *


def test_op_unlock_car():
    username, password, booking_number, car_number = "test_name", "1234343", "3434343", "A939N"
    res = op_unlock_car(username, password, booking_number, car_number)
    assert res.get("response") == "success"


def test_op_return_car():
    username, password, booking_number, return_car_number = "test_name", "1234343", "3434343", "A939N"
    res = op_return_car(username, password, booking_number, return_car_number)
    assert res.get("response") == "success"


def op_uplocation():
    username, password, latitude, longitude = "test_name", "1234343", "1.232323", "3.3434343"
    res = op_return_car(username, password, booking_number, return_car_number)
    assert res.get("response") == "success"
