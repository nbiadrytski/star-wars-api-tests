"""Contains common variables and constants used across the project."""

from pathlib import Path


THIS_FILE_PARENT_DIR = Path(__file__).parent.parent.absolute()
DATA_FILES_PATH = 'data/'

LOG_SEPARATOR = '\n' + 120 * '-' + '\n'

APP_HOST_ARG = '--app_host'
MAY_FORCE_ARG = '--may-force'

API_PATH = '/api'
PEOPLE_PATH = f'{API_PATH}/people/'
SEARCH_PARAM = 'search={}'

ASSERT_ERRORS = 'errors occurred:\n{}'
NOT_FOUND_RESP = {"detail": "Not found"}
RESPONSE_NOT_MATCH_MESSAGE = 'Responses do not match. Difference: {}. Actual response: {}'

APP_JSON_HEADER_VALUE = 'application/json'
CONTENT_TYPE_HEADER_NAME = 'Content-Type'
