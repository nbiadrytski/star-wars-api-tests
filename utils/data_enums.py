from enum import Enum


class Envs(Enum):
    SWAPI_PROD = 'https://swapi.py4e.com'


class HttpCodes(Enum):
    HTTP_200 = 200
    HTTP_404 = 404
