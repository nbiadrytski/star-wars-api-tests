from utils.constants import (
    APP_HOST_ARG,
    MAY_FORCE_ARG,
)


class Error(Exception):

    def __str__(self):
        return f'{self.message}'


class UnsupportedEnvException(Error):

    def __init__(self, env, supported_envs):
        self.message = f'\n"{env}" is not a supported environment.' \
                       f'\n Supported environments: {supported_envs}.'


class NoHostArgException(Error):

    def __init__(self, env):
        self.message = f'\nCommand line arg "{APP_HOST_ARG}" is missing. App host is {env}.'
