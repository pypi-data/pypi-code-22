# WARNING: Do not edit by hand, this file was generated by Crank:
#
#   https://github.com/gocardless/crank
#

class ApiResponse(object):
    """Response from the {{ .Config.api_name }} API, providing access
    to the status code, headers, and body.
    """

    def __init__(self, response):
        self._response = response

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def headers(self):
        return self._response.headers

    @property
    def body(self):
        return self._response.json()

