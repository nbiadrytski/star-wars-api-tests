import logging

from utils.http_utils import (
    ResponseHandler,
    Request
)
from utils.constants import LOG_SEPARATOR


class ApiClient:

    def __init__(self, app_host):
        self.app_host = app_host
        self.app_request = Request(self.app_host)
        self.logger = logging.getLogger(__name__)

    def get_request(self, api_path, query_params=None, check_status_code=True):
        if query_params:
            resp = self.app_request.get_request(api_path, query_params)
        else:
            resp = self.app_request.get_request(api_path)
        return self._response(resp, check_status_code)

    def _response(self, resp, check_status_code):
        if check_status_code:
            self.assert_http_status_code(resp, 200)
            self._log_http_response(resp)
            return resp
        self._log_http_response(resp)
        return resp

    def _log_http_response(self, resp):
        response_handler = ResponseHandler(resp)
        self.logger.debug('RESPONSE HEADERS: %s', response_handler.get_response_headers())
        self.logger.debug('RESPONSE BODY: %s%s', response_handler.get_text(), LOG_SEPARATOR)

    @staticmethod
    def assert_http_status_code(resp, code):
        response_handler = ResponseHandler(resp)
        status_code = response_handler.get_status_code()
        assert status_code == code, \
            f'Non-200 status code returned: {status_code}. Response: {response_handler.get_text()}'

    @staticmethod
    def get_value_from_json_response(resp, key):
        return ResponseHandler(resp).get_json_key_value(key)
