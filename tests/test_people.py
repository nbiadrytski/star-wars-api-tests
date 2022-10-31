import os

from pytest import (
    fixture,
    mark,
)

from utils.constants import (
    ASSERT_ERRORS,
    PEOPLE_PATH,
    NOT_FOUND_RESP,
    APP_JSON_HEADER_VALUE,
    CONTENT_TYPE_HEADER_NAME,
    THIS_FILE_PARENT_DIR,
    DATA_FILES_PATH,
    RESPONSE_NOT_MATCH_MESSAGE,
    SEARCH_PARAM,
)
from utils.helper_funcs import (
    generate_abc_numeric_params,
    timeit
)
from utils.data_enums import HttpCodes


CASE_INSENSITIVE_EXPECTED_COUNT = 3
CASE_INSENSITIVE_SEARCH_PARAM = SEARCH_PARAM.format('WaLkE')


@fixture
def people_objects_list(app_client):
    def people_objects_list_(query_params=None, check_status_code=True):
        return app_client.get_people_list(query_params, check_status_code)
    return people_objects_list_


@mark.people
@timeit(write_to_file=True)
def test_names_unique(people_objects_list):
    names_list = []
    for person in list(people_objects_list()):
        names_list.append(person['name'])
    assert len(names_list) == len(set(names_list)), f'Names should be unique. Actual names: {names_list}'


@mark.people
@timeit(write_to_file=False)
def test_search_case_insensitive(people_objects_list):
    people_list = list(people_objects_list(query_params=CASE_INSENSITIVE_SEARCH_PARAM))
    assert len(people_list) == CASE_INSENSITIVE_EXPECTED_COUNT, \
        f'Wrong number of person objects is returned ' \
        f'after searching people with {CASE_INSENSITIVE_SEARCH_PARAM} query param. ' \
        f'Actual person objects: {people_list}'


@mark.people
def test_search_count(app_client, get_value_from_json):
    actual_count = get_value_from_json(
        app_client.get_people(query_params=CASE_INSENSITIVE_SEARCH_PARAM), 'count'
    )
    assert actual_count == CASE_INSENSITIVE_EXPECTED_COUNT,\
        f'Expected {CASE_INSENSITIVE_EXPECTED_COUNT} count field ' \
        f'after searching people with {CASE_INSENSITIVE_SEARCH_PARAM} query param. Got: {actual_count}.'


@mark.people
def test_page_0_not_exist(app_client, assert_status_code_and_json_resp):
    errors = []
    people_resp = app_client.get_people(query_params='page=0', check_status_code=False)
    assert_status_code_and_json_resp(
        people_resp, HttpCodes.HTTP_404.value, PEOPLE_PATH, NOT_FOUND_RESP, errors
    )
    assert not errors, ASSERT_ERRORS.format('\n'.join(errors))


@mark.people
@mark.parametrize('search_param, expected_count',
                  [
                      (SEARCH_PARAM.format('Skywalker'), 3),
                      (SEARCH_PARAM.format('Vader'), 1),
                      (SEARCH_PARAM.format('Darth'), 2)
                  ],
                  ids=[
                      SEARCH_PARAM.format('Skywalker'),
                      SEARCH_PARAM.format('Vader'),
                      SEARCH_PARAM.format('Darth')]
                  )
def test_search_count(people_objects_list, search_param, expected_count):
    names_list = []
    for person in list(people_objects_list(query_params=search_param)):
        names_list.append(person['name'])
    assert len(names_list) == expected_count


@mark.people
def test_person_object_schema(people_objects_list, get_schema_required_fields):
    errors = []
    for person in list(people_objects_list()):
        for field in get_schema_required_fields('people'):
            if field not in person:
                errors.append(
                    (person['name'], f'id={person["url"][-2]}', f'{field} field is missing')
                )
    assert not errors, f'Person object required fields validation failed: {errors}'


@mark.people
@mark.parametrize('char, has_results', generate_abc_numeric_params())
def test_abc_nums_search(search_in_resource, get_value_from_json, char, has_results):
    results_list = get_value_from_json(search_in_resource('people', char), 'results')
    actual_result = len(results_list) > 0
    assert actual_result == has_results, \
        f'Results list should > 0 for ABC chars and numbers in range from 0 to 9 except 0, 6, 9.' \
        f' Actual results: {results_list}'


@mark.people
def test_non_existing_person(app_client, assert_status_code_and_json_resp, resp_header):
    errors = []
    person_resp = app_client.get_person(
        person_id=100, query_params=None, check_status_code=False
    )
    assert_status_code_and_json_resp(
        person_resp, HttpCodes.HTTP_404.value, PEOPLE_PATH, NOT_FOUND_RESP, errors
    )
    if resp_header(person_resp, CONTENT_TYPE_HEADER_NAME) != APP_JSON_HEADER_VALUE:
        errors.append(f'{CONTENT_TYPE_HEADER_NAME} header should have {APP_JSON_HEADER_VALUE} value')
    assert not errors, ASSERT_ERRORS.format('\n'.join(errors))


@mark.people
def test_wookiee_person(app_client, get_dicts_diff, resp_text):
    resp = app_client.get_person(1, 'format=wookiee')
    difference = get_dicts_diff(
        resp,
        os.path.join(THIS_FILE_PARENT_DIR, DATA_FILES_PATH, 'wookiee_person1.json'),
        None
    )
    assert not difference, RESPONSE_NOT_MATCH_MESSAGE.format(difference, resp_text(resp))
