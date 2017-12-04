# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Wrapper class for aiohttp request objects."""

from itertools import chain
from logging import getLogger

from .async_utils import run_coroutine
from .base import BaseRequest
from .ip_utils import get_real_user_ip

LOGGER = getLogger(__name__)


def multidict_to_dict(multidict):
    """Convert a multidict instance to a regular dict.

    Each key in the resulting dict is associated to the list of values mapped
    to this key in the original multidict.
    """
    return {key: multidict.getall(key) for key in multidict}


class AioHTTPRequest(BaseRequest):
    """Wrapper class for aiohttp request objects."""

    def __init__(self, request):
        super(AioHTTPRequest, self).__init__()
        self.request = request

        # Caches for lazy properties.
        self._headers = None
        self._query_params = None
        self._query_params_values = None
        self._form_params = None
        self._cookies_params = None
        self._json_params = None

        # Debug magic.
        if self.__class__.DEBUG_MODE is None:
            self.__class__.DEBUG_MODE = self.is_debug()

    def is_debug(self):
        """True if the application debug mode is enabled, False otherwise."""
        return self.request.app.debug

    @property
    def server_port(self):
        """Server port number."""
        sockname = self.request.transport.get_extra_info('sockname')
        return sockname[1]

    @property
    def remote_port(self):
        """Client port number."""
        peername = self.request.transport.get_extra_info('peername')
        return peername[1]

    @property
    def method(self):
        """Request method."""
        return self.request.method

    @property
    def scheme(self):
        """Request scheme (http or https)."""
        return self.request.scheme

    @property
    def hostname(self):
        """Request host."""
        return self.request.host

    @property
    def path(self):
        """Request path."""
        return self.request.path

    @property
    def headers(self):
        """Dictionary of request headers.

        Headers are encoded in WSGI format, described in PEP 3333.
        """
        if self._headers is None:
            headers = {
                'REQUEST_METHOD': self.request.method,
                'SCRIPT_NAME': '',  # Mandatory as per PEP 3333.
                'PATH_INFO': self.request.path,
                'QUERY_STRING': self.request.query_string,
                'CONTENT_TYPE': self.request.content_type,
                'SERVER_NAME': self.hostname,
                'SERVER_PORT': str(self.server_port),
                'SERVER_PROTOCOL': 'HTTP/{}.{}'.format(*self.request.version),
                'wsgi.scheme': self.request.scheme,
            }
            if self.request.content_length is not None:
                headers['CONTENT_LENGTH'] = str(self.request.content_length)
            for key, value in self.request.headers.items():
                name = 'HTTP_{}'.format(key.replace('-', '_').upper())
                headers[name] = value
            self._headers = headers
        return self._headers

    def get_header(self, name):
        """Get a specific WSGI header.

        Return None if the header is not set.
        """
        return self.headers.get(name)

    @property
    def referer(self):
        """Request referer."""
        return self.get_header('HTTP_REFERER')

    @property
    def client_user_agent(self):
        """User agent."""
        return self.get_header('HTTP_USER_AGENT')

    @property
    def client_ip(self):
        """Client IP address."""
        return get_real_user_ip(self.request.remote,
                                *self.iter_client_ips())

    @property
    def query_params(self):
        """Dictionary of query parameters."""
        if self._query_params is None:
            self._query_params = multidict_to_dict(self.request.query)
        return self._query_params

    @property
    def query_params_values(self):
        """Flat list of query values."""
        if self._query_params_values is None:
            self._query_params_values = list(chain.from_iterable(
                self.query_params.values()
            ))
        return self._query_params_values

    @property
    def form_params(self):
        """Dictionary of form parameters."""
        if self._form_params is None:
            post_params = run_coroutine(self.request.post())
            self._form_params = multidict_to_dict(post_params)
        return self._form_params

    @property
    def cookies_params(self):
        """Dictionary of cookies parameters."""
        if self._cookies_params is None:
            self._cookies_params = multidict_to_dict(self.request.cookies)
        return self._cookies_params

    @property
    def json_params(self):
        """Request body, decoded as JSON."""
        if self._json_params is None:
            try:
                json_params = run_coroutine(self.request.json())
                self._json_params = multidict_to_dict(json_params)
            except Exception:
                self._json_params = {}
        return self._json_params

    @property
    def view_params(self):
        """Dictionary of view arguments that matched the request."""
        return self.request.match_info
