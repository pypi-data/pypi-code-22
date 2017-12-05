# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np


from .abc import Codec
from .compat import ndarray_from_buffer, buffer_copy


class PackBits(Codec):
    """Codec to pack elements of a boolean array into bits in a uint8 array.

    Examples
    --------
    >>> import numcodecs
    >>> import numpy as np
    >>> codec = numcodecs.PackBits()
    >>> x = np.array([True, False, False, True], dtype=bool)
    >>> y = codec.encode(x)
    >>> y
    array([  4, 144], dtype=uint8)
    >>> z = codec.decode(y)
    >>> z
    array([ True, False, False,  True], dtype=bool)

    Notes
    -----
    The first element of the encoded array stores the number of bits that
    were padded to complete the final byte.

    """

    codec_id = 'packbits'

    def __init__(self):
        pass

    def encode(self, buf):

        # view input as ndarray
        arr = ndarray_from_buffer(buf, bool)

        # determine size of packed data
        n = arr.size
        n_bytes_packed = (n // 8)
        n_bits_leftover = n % 8
        if n_bits_leftover > 0:
            n_bytes_packed += 1

        # setup output
        enc = np.empty(n_bytes_packed + 1, dtype='u1')

        # store how many bits were padded
        if n_bits_leftover:
            n_bits_padded = 8 - n_bits_leftover
        else:
            n_bits_padded = 0
        enc[0] = n_bits_padded

        # apply encoding
        enc[1:] = np.packbits(arr)

        return enc

    def decode(self, buf, out=None):

        # view encoded data as ndarray
        enc = ndarray_from_buffer(buf, 'u1')

        # find out how many bits were padded
        n_bits_padded = int(enc[0])

        # apply decoding
        dec = np.unpackbits(enc[1:])

        # remove padded bits
        if n_bits_padded:
            dec = dec[:-n_bits_padded]

        # view as boolean array
        dec = dec.view(bool)

        # handle destination
        return buffer_copy(dec, out)
