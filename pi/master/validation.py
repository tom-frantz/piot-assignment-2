"""
Help methods for customised data validation.
"""

from decimal import Decimal


def latitude_decimal(value):
    try:
        Decimal(value)
    except:
        raise ValueError("Latitude value is not a valid decimal number.")

    if value > 90 or value < -90:
        raise ValueError("Latitude value out of range [-90,90].")

    return value


def longitude_decimal(value):
    try:
        Decimal(value)
    except:
        raise ValueError("Longitude value is not a valid decimal number.")

    if value > 180 or value < -180:
        raise ValueError('Longitude value out of range [-180, 180]')

    return value

def string_30(value):
    value = str(value)
    if len(value) > 30:
        raise ValueError("String length should be less than or equal to 30.")
    return value

def string_1000(value):
    value = str(value)
    if len(value > 1000):
        raise ValueError("Maximum length allowed: 1000 characters.")
    return value

def price(value, name):
    try:
        Decimal(value)
    except:
        raise ValueError("{} is not a valid decimal number".format(name))

    if value < 0:
        raise ValueError("Cost value should not be negative.")

    return value

def role(value):
    value = value.strip().lower()
    if value != "user" and value != "admin" and value != "engineer":
        raise ValueError("A valid role should be user, admin or engineer.")
    return value.strip().lower()