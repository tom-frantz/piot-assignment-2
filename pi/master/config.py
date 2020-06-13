"""
Flask App config profiles for:

- Development
- Testing
- Production
"""

import os

class Config(object):
    DEBUG = False
    TESTING = False
    DB_PASSWORD = os.environ["My_SQL"]

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234567@35.193.95.10:3306/IoT'.format(
        DB_PASSWORD
    )

    JWT_SECRET_KEY = 'jwt-secret-string'
    # app.config['JWT_BLACKLIST_ENABLED'] = True
    # app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    # SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    # DB_PASSWORD = os.environ["My_SQL"]
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@127.0.0.1:3306/CarShare'.format(
    #     DB_PASSWORD
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    JWT_SECRET_KEY = 'jwt_testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
