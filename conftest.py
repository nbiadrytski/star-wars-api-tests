import logging

from pytest import fixture
from dictdiffer import diff

from utils.data_enums import HttpCodes
from utils.helper_funcs import (
    get_host,
    convert_json_to_dict
)
from utils.constants import (
    APP_HOST_ARG,
    API_PATH,
    MAY_FORCE_ARG,
)
from utils.errors import NoHostArgException
from utils.clients import SwapiClient
from utils.http_utils import ResponseHandler


LOGGER = logging.getLogger(__name__)


def pytest_collection_finish():
    print('Come To The Dark Side!')


def pytest_runtest_logfinish():
    print('\nMay the Force Be With You')


def pytest_collection_modifyitems(items):
    """
    Automatically adds 'all' mark to all test functions.
    'all' mark is used to run all tests.
    -m mark_name
    -m "mark_name or mark_name or mark_name" to pass several marks.
    """
    for item in items:
        item.add_marker('all')


def pytest_addoption(parser):
    parser.addoption(APP_HOST_ARG, action='store', help='App host')
    parser.addoption(MAY_FORCE_ARG, action='store', default=False, help='May-Force arg')


@fixture(scope='session')
def app_host_arg(request):
    if request.config.getoption(APP_HOST_ARG) is None:
        raise NoHostArgException(request.config.getoption(APP_HOST_ARG))
    return request.config.getoption(APP_HOST_ARG)


@fixture(scope='session')
def may_force_arg(request):
    return request.config.getoption(MAY_FORCE_ARG)


@fixture(scope='session')
def app_host(app_host_arg, may_force_arg):
    application_host = get_host(app_host_arg)
    if isinstance(may_force_arg, str) and may_force_arg.lower() == "true":
        print('\nWe have cookies!')
    LOGGER.info('App host: %s', application_host)
    return application_host


@fixture(scope='session')
def app_client(app_host):
    return SwapiClient(app_host)


@fixture
def get_value_from_json():
    def get_value_from_json_(resp, json_path):
        return ResponseHandler(resp).get_json_key_value(json_path)

    return get_value_from_json_


@fixture
def status_code():
    def status_code_(resp):
        return ResponseHandler(resp).get_status_code()
    return status_code_


@fixture
def resp_json():
    def resp_json_(resp):
        return ResponseHandler(resp).get_json()
    return resp_json_


@fixture
def resp_text():
    def resp_text_(resp):
        return ResponseHandler(resp).get_text()
    return resp_text_


@fixture
def resp_header():
    def resp_header_(resp, header_name):
        return ResponseHandler(resp).get_response_header(header_name)
    return resp_header_


@fixture
def search_in_resource(app_client):
    def search_in_resource_(resource, search_item):
        return app_client.get_request(f'{API_PATH}/{resource}/', f'search={search_item}')
    return search_in_resource_


@fixture
def get_schema_required_fields(app_client, get_value_from_json):
    def get_schema_required_fields_(resource):
        resp = app_client.get_schema(resource)
        return get_value_from_json(resp, "required")
    return get_schema_required_fields_


@fixture
def assert_status_code_and_json_resp(status_code, resp_json):
    def assert_status_code_and_json_resp_(
            actual_resp, expected_status_code, api_path, expected_resp, errors_list
    ):
        actual_status_code = status_code(actual_resp)
        actual_resp = resp_json(actual_resp)
        if actual_status_code != expected_status_code:
            errors_list.append(
                f'GET {api_path} should return {HttpCodes.HTTP_404} status code. Got: {actual_status_code}'
            )
        if actual_resp != expected_resp:
            errors_list.append(f'GET {api_path} should return {expected_resp}. Got: {actual_resp}')
    return assert_status_code_and_json_resp_


@fixture
def get_dicts_diff(resp_json):
    """
    Converts Response object to actual_dict and expected_json_file to expected_dict.
    Optionally, ignores keys passed to 'ignore' param of diff().
    'ignore' param must be a set of keys where each key is a list element, e.g.
    ignore=(['results', 0, 'processingTimeMS'],).
    Returns a difference list of two dicts.
    """
    def get_dicts_diff(resp, expected_json_file, set_of_ignored_keys):
        expected_dict = convert_json_to_dict(expected_json_file)
        result = diff(
            resp_json(resp), expected_dict, ignore=set_of_ignored_keys
        )
        return list(result)
    return get_dicts_diff
