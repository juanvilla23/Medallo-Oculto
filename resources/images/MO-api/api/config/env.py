import os
from ..patterns.singleton import SingletonMeta

class ENV_VARIABLES(metaclass=SingletonMeta):

    DATABASE_CONECTION = os.getenv('DATABASE_CONECTION')
    API_NAME = os.getenv('API_NAME')
    JWT_SECRET = os.getenv('JWT_SECRET') # The JWT secret string
    LOCALHOST_SERVER_URL = os.getenv('LOCALHOST_SERVER_URL')