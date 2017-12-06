# Copyright 2016-present MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for working with the BSON decimal128 type.

.. versionadded:: 3.4

.. note:: The Decimal128 BSON type requires MongoDB 3.4+.
"""

import decimal
import struct
import sys

from bson.py3compat import (PY3 as _PY3,
                            string_type as _string_type)


if _PY3:
    _from_bytes = int.from_bytes  # pylint: disable=no-member, invalid-name
else:
    import binascii
    def _from_bytes(value, dummy, _int=int, _hexlify=binascii.hexlify):
        "An implementation of int.from_bytes for python 2.x."
        return _int(_hexlify(value), 16)

if sys.version_info[:2] == (2, 6):
    def _bit_length(num):
        """bit_length for python 2.6"""
        if num:
            # bin() was new in 2.6. Note that this won't work
            # for values less than 0, which we never have here.
            return len(bin(num)) - 2
        # bit_length(0) is 0, but len(bin(0)) - 2 is 1
        return 0
else:
    def _bit_length(num):
        """bit_length for python >= 2.7"""
        # num could be int or long in python 2.7
        return num.bit_length()


_PACK_64 = struct.Struct("<Q").pack
_UNPACK_64 = struct.Struct("<Q").unpack

_EXPONENT_MASK = 3 << 61
_EXPONENT_BIAS = 6176
_EXPONENT_MAX = 6144
_EXPONENT_MIN = -6143
_MAX_DIGITS = 34

_INF = 0x7800000000000000
_NAN = 0x7c00000000000000
_SNAN = 0x7e00000000000000
_SIGN = 0x8000000000000000

_NINF = (_INF + _SIGN, 0)
_PINF = (_INF, 0)
_NNAN = (_NAN + _SIGN, 0)
_PNAN = (_NAN, 0)
_NSNAN = (_SNAN + _SIGN, 0)
_PSNAN = (_SNAN, 0)

_CTX_OPTIONS = {
    'prec': _MAX_DIGITS,
    'rounding': decimal.ROUND_HALF_EVEN,
    'Emin': _EXPONENT_MIN,
    'Emax': _EXPONENT_MAX,
    'capitals': 1,
    'flags': [],
    'traps': [decimal.InvalidOperation,
              decimal.Overflow,
              decimal.Inexact]
}

try:
    # Python >= 3.3, cdecimal
    decimal.Context(clamp=1)  # pylint: disable=unexpected-keyword-arg
    _CTX_OPTIONS['clamp'] = 1
except TypeError:
    # Python < 3.3
    _CTX_OPTIONS['_clamp'] = 1

_DEC128_CTX = decimal.Context(**_CTX_OPTIONS.copy())


def create_decimal128_context():
    """Returns an instance of :class:`decimal.Context` appropriate
    for working with IEEE-754 128-bit decimal floating point values.
    """
    opts = _CTX_OPTIONS.copy()
    opts['traps'] = []
    return decimal.Context(**opts)


def _decimal_to_128(value):
    """Converts a decimal.Decimal to BID (high bits, low bits).

    :Parameters:
      - `value`: An instance of decimal.Decimal
    """
    with decimal.localcontext(_DEC128_CTX) as ctx:
        value = ctx.create_decimal(value)

    if value.is_infinite():
        return _NINF if value.is_signed() else _PINF

    sign, digits, exponent = value.as_tuple()

    if value.is_nan():
        if digits:
            raise ValueError("NaN with debug payload is not supported")
        if value.is_snan():
            return _NSNAN if value.is_signed() else _PSNAN
        return _NNAN if value.is_signed() else _PNAN

    significand = int("".join([str(digit) for digit in digits]))
    bit_length = _bit_length(significand)

    high = 0
    low = 0
    for i in range(min(64, bit_length)):
        if significand & (1 << i):
            low |= 1 << i

    for i in range(64, bit_length):
        if significand & (1 << i):
            high |= 1 << (i - 64)

    biased_exponent = exponent + _EXPONENT_BIAS

    if high >> 49 == 1:
        high = high & 0x7fffffffffff
        high |= _EXPONENT_MASK
        high |= (biased_exponent & 0x3fff) << 47
    else:
        high |= biased_exponent << 49

    if sign:
        high |= _SIGN

    return high, low


class Decimal128(object):
    """BSON Decimal128 type::

      >>> Decimal128(Decimal("0.0005"))
      Decimal128('0.0005')
      >>> Decimal128("0.0005")
      Decimal128('0.0005')
      >>> Decimal128((3474527112516337664, 5))
      Decimal128('0.0005')

    :Parameters:
      - `value`: An instance of :class:`decimal.Decimal`, string, or tuple of
        (high bits, low bits) from Binary Integer Decimal (BID) format.

    .. note:: :class:`~Decimal128` uses an instance of :class:`decimal.Context`
      configured for IEEE-754 Decimal128 when validating parameters.
      Signals like :class:`decimal.InvalidOperation`, :class:`decimal.Inexact`,
      and :class:`decimal.Overflow` are trapped and raised as exceptions::

        >>> Decimal128(".13.1")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ...
        decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]
        >>>
        >>> Decimal128("1E-6177")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ...
        decimal.Inexact: [<class 'decimal.Inexact'>]
        >>>
        >>> Decimal128("1E6145")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          ...
        decimal.Overflow: [<class 'decimal.Overflow'>, <class 'decimal.Rounded'>]

      To ensure the result of a calculation can always be stored as BSON
      Decimal128 use the context returned by
      :func:`create_decimal128_context`::

        >>> import decimal
        >>> decimal128_ctx = create_decimal128_context()
        >>> with decimal.localcontext(decimal128_ctx) as ctx:
        ...     Decimal128(ctx.create_decimal(".13.3"))
        ...
        Decimal128('NaN')
        >>>
        >>> with decimal.localcontext(decimal128_ctx) as ctx:
        ...     Decimal128(ctx.create_decimal("1E-6177"))
        ...
        Decimal128('0E-6176')
        >>>
        >>> with decimal.localcontext(DECIMAL128_CTX) as ctx:
        ...     Decimal128(ctx.create_decimal("1E6145"))
        ...
        Decimal128('Infinity')

      To match the behavior of MongoDB's Decimal128 implementation
      str(Decimal(value)) may not match str(Decimal128(value)) for NaN values::

        >>> Decimal128(Decimal('NaN'))
        Decimal128('NaN')
        >>> Decimal128(Decimal('-NaN'))
        Decimal128('NaN')
        >>> Decimal128(Decimal('sNaN'))
        Decimal128('NaN')
        >>> Decimal128(Decimal('-sNaN'))
        Decimal128('NaN')

      However, :meth:`~Decimal128.to_decimal` will return the exact value::

        >>> Decimal128(Decimal('NaN')).to_decimal()
        Decimal('NaN')
        >>> Decimal128(Decimal('-NaN')).to_decimal()
        Decimal('-NaN')
        >>> Decimal128(Decimal('sNaN')).to_decimal()
        Decimal('sNaN')
        >>> Decimal128(Decimal('-sNaN')).to_decimal()
        Decimal('-sNaN')

      Two instances of :class:`Decimal128` compare equal if their Binary
      Integer Decimal encodings are equal::

        >>> Decimal128('NaN') == Decimal128('NaN')
        True
        >>> Decimal128('NaN').bid == Decimal128('NaN').bid
        True

      This differs from :class:`decimal.Decimal` comparisons for NaN::

        >>> Decimal('NaN') == Decimal('NaN')
        False
    """
    __slots__ = ('__high', '__low')

    _type_marker = 19

    def __init__(self, value):
        if isinstance(value, (_string_type, decimal.Decimal)):
            self.__high, self.__low = _decimal_to_128(value)
        elif isinstance(value, (list, tuple)):
            if len(value) != 2:
                raise ValueError('Invalid size for creation of Decimal128 '
                                 'from list or tuple. Must have exactly 2 '
                                 'elements.')
            self.__high, self.__low = value
        else:
            raise TypeError("Cannot convert %r to Decimal128" % (value,))

    def to_decimal(self):
        """Returns an instance of :class:`decimal.Decimal` for this
        :class:`Decimal128`.
        """
        high = self.__high
        low = self.__low
        sign = 1 if (high & _SIGN) else 0

        if (high & _SNAN) == _SNAN:
            return decimal.Decimal((sign, (), 'N'))
        elif (high & _NAN) == _NAN:
            return decimal.Decimal((sign, (), 'n'))
        elif (high & _INF) == _INF:
            return decimal.Decimal((sign, (), 'F'))

        if (high & _EXPONENT_MASK) == _EXPONENT_MASK:
            exponent = ((high & 0x1fffe00000000000) >> 47) - _EXPONENT_BIAS
            return decimal.Decimal((sign, (0,), exponent))
        else:
            exponent = ((high & 0x7fff800000000000) >> 49) - _EXPONENT_BIAS

        arr = bytearray(15)
        mask = 0x00000000000000ff
        for i in range(14, 6, -1):
            arr[i] = (low & mask) >> ((14 - i) << 3)
            mask = mask << 8

        mask = 0x00000000000000ff
        for i in range(6, 0, -1):
            arr[i] = (high & mask) >> ((6 - i) << 3)
            mask = mask << 8

        mask = 0x0001000000000000
        arr[0] = (high & mask) >> 48

        # Have to convert bytearray to bytes for python 2.6.
        # cdecimal only accepts a tuple for digits.
        digits = tuple(
            int(digit) for digit in str(_from_bytes(bytes(arr), 'big')))

        with decimal.localcontext(_DEC128_CTX) as ctx:
            return ctx.create_decimal((sign, digits, exponent))

    @classmethod
    def from_bid(cls, value):
        """Create an instance of :class:`Decimal128` from Binary Integer
        Decimal string.

        :Parameters:
          - `value`: 16 byte string (128-bit IEEE 754-2008 decimal floating
            point in Binary Integer Decimal (BID) format).
        """
        if not isinstance(value, bytes):
            raise TypeError("value must be an instance of bytes")
        if len(value) != 16:
            raise ValueError("value must be exactly 16 bytes")
        return cls((_UNPACK_64(value[8:])[0], _UNPACK_64(value[:8])[0]))

    @property
    def bid(self):
        """The Binary Integer Decimal (BID) encoding of this instance."""
        return _PACK_64(self.__low) + _PACK_64(self.__high)

    def __str__(self):
        dec = self.to_decimal()
        if dec.is_nan():
            # Required by the drivers spec to match MongoDB behavior.
            return "NaN"
        return str(dec)

    def __repr__(self):
        return "Decimal128('%s')" % (str(self),)

    def __setstate__(self, value):
        self.__high, self.__low = value

    def __getstate__(self):
        return self.__high, self.__low

    def __eq__(self, other):
        if isinstance(other, Decimal128):
            return self.bid == other.bid
        return NotImplemented

    def __ne__(self, other):
        return not self == other
