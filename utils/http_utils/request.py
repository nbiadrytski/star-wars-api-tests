from urllib.parse import urljoin
import logging

import requests


class Request:
    """
    Wrapper around requests module.

    Parameters
    ----------
    host : str
        App hostname

    Attributes
    ----------
    host : str
         App hostname
    logger : logging.Logger
        Inits Logger object
    """

    def __init__(self, host):
        self.host = host
        self.logger = logging.getLogger(__name__)

    def get_request(self, path='', query_params=None):
        """
        Performs HTTP GET request.

        Parameters
        ----------
        path : str
            Endpoint path, e.g. api/people. Empty string by default
        query_params : dict or str or list of tuples
            Query params, e.g. {'param': 'value'}, 'param=value', (param, value).
            None by default

        Returns
        -------
        response : requests.models.Response
            Response returned by GET request
        """
        self.logger.debug('QUERY PARAMS: %s', query_params)
        return requests.get(
            url=urljoin(self.host, path), params=query_params, allow_redirects=True,
        )
