import os

from pytest import mark

from utils.constants import (
    THIS_FILE_PARENT_DIR,
    DATA_FILES_PATH,
    RESPONSE_NOT_MATCH_MESSAGE
)


@mark.root
def test_wookiee_person(app_client, get_dicts_diff, resp_text):
    resp = app_client.get_resources()
    difference = get_dicts_diff(
        resp,
        os.path.join(THIS_FILE_PARENT_DIR, DATA_FILES_PATH, 'resources.json'),
        None
    )
    assert not difference, RESPONSE_NOT_MATCH_MESSAGE.format(difference, resp_text(resp))
