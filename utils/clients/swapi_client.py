from utils.constants import API_PATH
from utils.http_utils import ApiClient


CALLED_ENDPOINT_LOG_MESSAGE = 'Called GET {} endpoint.'


class SwapiClient(ApiClient):

    def __init__(self, app_host):
        super().__init__(app_host)

    def get_people(self, query_params=None, check_status_code=True):
        path = f'{API_PATH}/people/'
        resp = self.get_request(path, query_params, check_status_code)
        self.logger.info(CALLED_ENDPOINT_LOG_MESSAGE.format(path))
        return resp

    def get_person(self, person_id, query_params=None, check_status_code=True):
        path = f'{API_PATH}/people/{person_id}'
        resp = self.get_request(path, query_params, check_status_code)
        self.logger.info(CALLED_ENDPOINT_LOG_MESSAGE.format(path))
        return resp

    def get_people_list(self, query_params=None, check_status_code=True):
        return self.get_value_from_json_response(
            self.get_people(query_params, check_status_code), 'results'
        )

    def get_schema(self, resource):
        path = f'{API_PATH}/{resource}/schema'
        resp = self.get_request(path)
        self.logger.info(CALLED_ENDPOINT_LOG_MESSAGE.format(path))
        return resp

    def get_resources(self,):
        path = f'{API_PATH}/'
        resp = self.get_request(path)
        self.logger.info(CALLED_ENDPOINT_LOG_MESSAGE.format(path))
        return resp
