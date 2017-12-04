# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Record request context."""

from logging import getLogger

from ..frameworks.aiohttp_framework import AioHTTPRequest
from ..runtime_storage import runtime
from .record_request_context import RecordRequestContext

LOGGER = getLogger(__name__)


class RecordRequestContextAioHTTP(RecordRequestContext):
    """Record request context."""

    def pre(self, original, request):
        self._store_request(AioHTTPRequest(request))

    def post(self, *args, **kwargs):
        runtime.clear_request()

    def failing(self, *args, **kwargs):
        runtime.clear_request()
