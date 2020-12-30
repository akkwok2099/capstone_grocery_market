import os
from dotenv import load_dotenv
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
load_dotenv(join(basedir, '.env'))


class Config(object):
    USER = os.environ.get('POSTGRES.USER')
    PASSWD = os.environ.get('POSTGRES.PASSWD')
    HOST = os.environ.get('POSTGRES.HOST')
    PORT = os.environ.get('POSTGRES.PORT')
    DB = os.environ.get('POSTGRES.DB')
    DBTEST = os.environ.get('POSTGRES.DB_TEST')

    SQLALCHEMY_DATABASE_URI = \
        "postgresql://{}:{}@{}:{}/{}".format(USER, PASSWD, HOST, PORT, DB)
    SQLALCHEMY_TEST_DATABASE_URI = \
        "postgresql://{}:{}@{}:{}/{}".format(USER, PASSWD, HOST, PORT, DBTEST)

    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    ALGORITHMS = os.environ.get('ALGORITHMS')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    API_AUDIENCE = os.environ.get('API_AUDIENCE')
    ACCESS_TOKEN_URL = os.environ.get('ACCESS_TOKEN_URL')
    AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
    CALLBACK_URL = os.environ.get('CALLBACK_URL')
    JWT_PAYLOAD = os.environ.get('JWT_PAYLOAD')
    PROFILE_KEY = os.environ.get('PROFILE_KEY')
    ID_KEY = os.environ.get('TOKENA_KEY')
    ACCESS_KEY = os.environ.get('TOKENB_KEY')
    ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE')
    SWAGGER_URL = os.environ.get('SWAGGER_URL')
    API_URL = os.environ.get('API_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    TEST_TOKEN = os.environ.get("TEST_TOKEN")
