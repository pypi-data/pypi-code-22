from __future__ import absolute_import, division, print_function

import warnings

from stripe import api_requestor, util
from stripe.api_resources.abstract import DeletableAPIResource


class EphemeralKey(DeletableAPIResource):
    OBJECT_NAME = 'ephemeral_key'

    @classmethod
    def class_name(cls):
        return 'ephemeral_key'

    @classmethod
    def create(cls, api_key=None, idempotency_key=None,
               stripe_version=None, stripe_account=None,
               api_version=None, **params):
        if stripe_version is None:
            if api_version is not None:
                stripe_version = api_version
                warnings.warn(
                    "The `api_version` parameter when creating an ephemeral "
                    "key is deprecated. Please use `stripe_version` instead.",
                    DeprecationWarning)
            else:
                raise ValueError(
                    "stripe_version must be specified to create an ephemeral "
                    "key")

        requestor = api_requestor.APIRequestor(
            api_key,
            api_version=stripe_version,
            account=stripe_account
        )

        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request('post', url, params, headers)
        return util.convert_to_stripe_object(response, api_key, stripe_version,
                                             stripe_account)
