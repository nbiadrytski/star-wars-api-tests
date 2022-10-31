from utils.helper_funcs import (
    file_content,
    get_value_by_json_path
)


class ResponseHandler:
    """
    Processes HTTP response.

    Parameters
    ----------
    resp : requests.models.Response
        Response object

    Attributes
    ----------
    resp : requests.models.Response
        Response object
    """

    def __init__(self, resp):
        self.resp = resp

    def get_status_code(self):
        return self.resp.status_code

    def get_response_headers(self):
        return self.resp.headers

    def get_json(self):
        return self.resp.json()

    def get_content(self):
        return self.resp.content

    def get_response_header(self, header_name):
        return self.resp.headers[header_name]

    def response_equals(self, expected_response):
        expected_response = file_content(expected_response)
        return self.resp.text == expected_response

    def get_text(self):
        return self.resp.text

    def get_json_key_value(self, json_path):
        return get_value_by_json_path(self.resp.json(), json_path)
