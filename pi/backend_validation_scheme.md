# Backend Validation Scheme

## Users and auth

- username:
  - type: str
  - length: 3-15
  - required: yes
  - **Primary key**
  - Regex: `^[A-Za-z0-9-_]{3,15}$`
- password:
  - type: str
  - length: 8-30
  - required: yes
  - Regex:`^[A-Za-z0-9-_]{8,30}$`
- facial recognition data:
  - _TBD_
- first_name:
  - type: str
  - length: 1-30
  - required: yes
  - Regex: `^[A-Za-z0-9-_]{1,30}$`
- last_name:
  - type: str
  - length: 1-30
  - required: yes
  - Regex: `^[A-Za-z0-9-_]{1,30}$`
- email:
  - type: str
  - Length: 100
  - Required: yes
  - Regex: `^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,6})$`
- role (**TBD**):
  - type: list
  - values: [user, engineer, admin]

## Cars

- car_number:
  - type: str
  - length: 6
  - required: yes
  - **Primary key**
  - Regex: `^[A-Za-z0-9]{1,6}$`
- seats (optional)
  - type: int
  - Max: 12
  - `inputs.int_interval(1,12)`

## Bookings

- booking_id
  - type: int, auto-increment from 1
  - required: yes
  - **Primary key**: yes
- username:
  - type: str
  - length: 3-15
  - required: yes
  - **Foreign key: Users**
- car_number:
  - type: str
  - length: 6
  - required: yes
  - **Foreign key: Cars**
- departure_time:
  - type: DateTime
  - required: yes
- return_time:
  - type: DateTime
  - required: yes
