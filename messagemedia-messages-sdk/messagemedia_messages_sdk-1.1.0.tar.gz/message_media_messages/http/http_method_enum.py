# -*- coding: utf-8 -*-

"""
    message_media_messages.http.http_method_enum


"""

class HttpMethodEnum(object):

    """Enumeration of an HTTP Method

    Attributes:
        GET: A GET Request
        POST: A POST Request
        PUT: A PUT Request
        PATCH: A PATCH Request
        DELETE: A DELETE Request

    """

    GET = "GET"

    POST = "POST"

    PUT = "PUT"

    PATCH = "PATCH"

    DELETE = "DELETE"

    @classmethod
    def to_string(cls, val):
        # Returns the string equivalent for the Enum.
        for k, v in list(vars(cls).items()):
            if v == val:
                return k

    @classmethod
    def from_string(cls, string):
        # Creates an instance of the Enum from a given string.
        return getattr(cls, string.upper(), None)
