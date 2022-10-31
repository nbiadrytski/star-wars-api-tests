import logging
import os
from string import ascii_lowercase
from functools import wraps
import time
import json

from jsonpath_rw import parse as json_parser

from utils.data_enums import Envs
from utils.errors import UnsupportedEnvException


LOGGER = logging.getLogger(__name__)


def get_host(env):
    env = env.upper()
    if env not in Envs.__members__:
        raise UnsupportedEnvException(env, Envs.__members__.keys())

    return Envs.__members__.get(env).value


def file_content(file_path):
    file_ = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(file_):
        with open(file_) as f:
            return f.read()
    else:
        LOGGER.error('File %s was not found', file_)
        raise FileNotFoundError


def get_value_by_json_path(actual_json, json_path, idx=0):
    try:
        return [match.value for match in json_parser(json_path).find(actual_json)][idx]
    except IndexError as error:
        LOGGER.error(
            'Did not find key value by json_path "%s" in response: %s',
            json_path, actual_json, exc_info=True
        )
        raise ValueError(
            f'Did not find key value by json_path "{json_path}"'
            f' in response: "{actual_json}". Error {error}')


def generate_abc_numeric_params():
    results = []
    for char in list(ascii_lowercase):
        results.append((char, True))
    for num in range(10):
        if num == 0 or num == 6 or num == 9:
            results.append((num, False))
        else:
            results.append((num, True))
    return results


def timeit(write_to_file=False):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            message = f'Function {func.__name__} took {total_time:.4f} seconds'
            LOGGER.info(message)
            if write_to_file:
                with open(f'results/{func.__name__}.log', 'w') as f:
                    f.write(message)
            return result
        return wrapper
    return decorate


def convert_json_to_dict(file_path):
    """
    Deserializes file-like object containing a JSON document to a dict

    Parameters
    ----------
    file_path : str
        Relative path to .json file

    Returns
    -------
    dictionary : dict
        Python dictionary
    """
    file_ = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(file_):
        with open(file_) as f:
            return json.load(f)
    else:
        LOGGER.error('File %s was not found', file_)
        raise FileNotFoundError
