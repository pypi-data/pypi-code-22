from __future__ import absolute_import, division, print_function

import hmac
import io
import logging
import sys
import os
import re

import stripe
from stripe import six


STRIPE_LOG = os.environ.get('STRIPE_LOG')

logger = logging.getLogger('stripe')

__all__ = [
    'io',
    'parse_qsl',
    'json',
    'utf8',
    'log_info',
    'log_debug',
    'dashboard_link',
    'logfmt',
]

try:
    from stripe.six.moves.urllib.parse import parse_qsl
except ImportError:
    # Python < 2.6
    from cgi import parse_qsl

try:
    import json
except ImportError:
    json = None

if not (json and hasattr(json, 'loads')):
    try:
        import simplejson as json
    except ImportError:
        if not json:
            raise ImportError(
                "Stripe requires a JSON library, such as simplejson. "
                "HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' or "
                "'easy_install simplejson', or contact support@stripe.com "
                "with questions.")
        else:
            raise ImportError(
                "Stripe requires a JSON library with the same interface as "
                "the Python 2.6 'json' library.  You appear to have a 'json' "
                "library with a different interface.  Please install "
                "the simplejson library.  HINT: Try installing the "
                "python simplejson library via 'pip install simplejson' "
                "or 'easy_install simplejson', or contact support@stripe.com"
                "with questions.")


def utf8(value):
    # Note the ordering of these conditionals: `unicode` isn't a symbol in
    # Python 3 so make sure to check version before trying to use it. Python
    # 2to3 will also boil out `unicode`.
    if six.PY2 and isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


def is_appengine_dev():
    return ('APPENGINE_RUNTIME' in os.environ and
            'Dev' in os.environ.get('SERVER_SOFTWARE', ''))


def _console_log_level():
    if stripe.log in ['debug', 'info']:
        return stripe.log
    elif STRIPE_LOG in ['debug', 'info']:
        return STRIPE_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == 'debug':
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ['debug', 'info']:
        print(msg, file=sys.stderr)
    logger.info(msg)


def _test_or_live_environment():
    if stripe.api_key is None:
        return
    match = re.match(r'sk_(live|test)_', stripe.api_key)
    if match is None:
        return
    return match.groups()[0]


def dashboard_link(request_id):
    return 'https://dashboard.stripe.com/{env}/logs/{reqid}'.format(
        env=_test_or_live_environment() or 'test',
        reqid=request_id,
    )


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if six.PY3 and hasattr(val, 'decode'):
            val = val.decode('utf-8')
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if not isinstance(val, six.string_types):
            val = six.text_type(val)
        if re.search(r'\s', val):
            val = repr(val)
        # key should already be a string
        if re.search(r'\s', key):
            key = repr(key)
        return u'{key}={val}'.format(key=key, val=val)
    return u' '.join([fmt(key, val) for key, val in sorted(props.items())])


# Borrowed from Django's source code
if hasattr(hmac, 'compare_digest'):
    # Prefer the stdlib implementation, when available.
    def secure_compare(val1, val2):
        return hmac.compare_digest(utf8(val1), utf8(val2))
else:
    def secure_compare(val1, val2):
        """
        Returns True if the two strings are equal, False otherwise.
        The time taken is independent of the number of characters that match.
        For the sake of simplicity, this function executes in constant time
        only when the two strings have the same length. It short-circuits when
        they have different lengths.
        """
        val1, val2 = utf8(val1), utf8(val2)
        if len(val1) != len(val2):
            return False
        result = 0
        if six.PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
            for x, y in zip(val1, val2):
                result |= x ^ y
        else:
            for x, y in zip(val1, val2):
                result |= ord(x) ^ ord(y)
        return result == 0


OBJECT_CLASSES = {}


def load_object_classes():
    # This is here to avoid a circular dependency
    from stripe import api_resources

    global OBJECT_CLASSES

    OBJECT_CLASSES = {
        # data structures
        api_resources.ListObject.OBJECT_NAME: api_resources.ListObject,

        # business objects
        api_resources.Account.OBJECT_NAME: api_resources.Account,
        api_resources.AlipayAccount.OBJECT_NAME: api_resources.AlipayAccount,
        api_resources.ApplePayDomain.OBJECT_NAME: api_resources.ApplePayDomain,
        api_resources.ApplicationFee.OBJECT_NAME: api_resources.ApplicationFee,
        api_resources.ApplicationFeeRefund.OBJECT_NAME:
            api_resources.ApplicationFeeRefund,
        api_resources.Balance.OBJECT_NAME: api_resources.Balance,
        api_resources.BalanceTransaction.OBJECT_NAME:
            api_resources.BalanceTransaction,
        api_resources.BankAccount.OBJECT_NAME: api_resources.BankAccount,
        api_resources.BitcoinReceiver.OBJECT_NAME:
            api_resources.BitcoinReceiver,
        api_resources.BitcoinTransaction.OBJECT_NAME:
            api_resources.BitcoinTransaction,
        api_resources.Card.OBJECT_NAME: api_resources.Card,
        api_resources.Charge.OBJECT_NAME: api_resources.Charge,
        api_resources.CountrySpec.OBJECT_NAME: api_resources.CountrySpec,
        api_resources.Coupon.OBJECT_NAME: api_resources.Coupon,
        api_resources.Customer.OBJECT_NAME: api_resources.Customer,
        api_resources.Dispute.OBJECT_NAME: api_resources.Dispute,
        api_resources.EphemeralKey.OBJECT_NAME: api_resources.EphemeralKey,
        api_resources.Event.OBJECT_NAME: api_resources.Event,
        api_resources.ExchangeRate.OBJECT_NAME: api_resources.ExchangeRate,
        api_resources.FileUpload.OBJECT_NAME: api_resources.FileUpload,
        api_resources.Invoice.OBJECT_NAME: api_resources.Invoice,
        api_resources.InvoiceItem.OBJECT_NAME: api_resources.InvoiceItem,
        api_resources.LoginLink.OBJECT_NAME: api_resources.LoginLink,
        api_resources.Order.OBJECT_NAME: api_resources.Order,
        api_resources.OrderReturn.OBJECT_NAME: api_resources.OrderReturn,
        api_resources.Payout.OBJECT_NAME: api_resources.Payout,
        api_resources.Plan.OBJECT_NAME: api_resources.Plan,
        api_resources.Product.OBJECT_NAME: api_resources.Product,
        api_resources.Recipient.OBJECT_NAME: api_resources.Recipient,
        api_resources.RecipientTransfer.OBJECT_NAME:
            api_resources.RecipientTransfer,
        api_resources.Refund.OBJECT_NAME: api_resources.Refund,
        api_resources.Reversal.OBJECT_NAME: api_resources.Reversal,
        api_resources.SKU.OBJECT_NAME: api_resources.SKU,
        api_resources.Source.OBJECT_NAME: api_resources.Source,
        api_resources.SourceTransaction.OBJECT_NAME:
            api_resources.SourceTransaction,
        api_resources.Subscription.OBJECT_NAME: api_resources.Subscription,
        api_resources.SubscriptionItem.OBJECT_NAME:
            api_resources.SubscriptionItem,
        api_resources.ThreeDSecure.OBJECT_NAME: api_resources.ThreeDSecure,
        api_resources.Token.OBJECT_NAME: api_resources.Token,
        api_resources.Transfer.OBJECT_NAME: api_resources.Transfer,
    }


def convert_to_stripe_object(resp, api_key=None, stripe_version=None,
                             stripe_account=None):
    global OBJECT_CLASSES

    if len(OBJECT_CLASSES) == 0:
        load_object_classes()
    types = OBJECT_CLASSES.copy()

    if isinstance(resp, list):
        return [convert_to_stripe_object(i, api_key, stripe_version,
                                         stripe_account) for i in resp]
    elif isinstance(resp, dict) and \
            not isinstance(resp, stripe.stripe_object.StripeObject):
        resp = resp.copy()
        klass_name = resp.get('object')
        if isinstance(klass_name, six.string_types):
            klass = types.get(klass_name, stripe.stripe_object.StripeObject)
        else:
            klass = stripe.stripe_object.StripeObject
        return klass.construct_from(resp, api_key,
                                    stripe_version=stripe_version,
                                    stripe_account=stripe_account)
    else:
        return resp


def convert_array_to_dict(arr):
    if isinstance(arr, list):
        d = {}
        for i, value in enumerate(arr):
            d[str(i)] = value
        return d
    else:
        return arr


def populate_headers(idempotency_key):
    if idempotency_key is not None:
        return {"Idempotency-Key": idempotency_key}
    return None
