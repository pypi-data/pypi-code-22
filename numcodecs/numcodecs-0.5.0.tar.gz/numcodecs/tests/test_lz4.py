# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division
import itertools


import numpy as np


from numcodecs.lz4 import LZ4
from numcodecs.tests.common import (check_encode_decode, check_config, check_repr,
                                    check_backwards_compatibility,
                                    check_err_decode_object_buffer,
                                    check_err_encode_object_buffer)


codecs = [
    LZ4(),
    LZ4(acceleration=-1),
    LZ4(acceleration=0),
    LZ4(acceleration=1),
    LZ4(acceleration=10),
    LZ4(acceleration=100),
    LZ4(acceleration=1000000),
]


# mix of dtypes: integer, float, bool, string
# mix of shapes: 1D, 2D, 3D
# mix of orders: C, F
arrays = [
    np.arange(1000, dtype='i4'),
    np.linspace(1000, 1001, 1000, dtype='f8'),
    np.random.normal(loc=1000, scale=1, size=(100, 10)),
    np.random.randint(0, 2, size=1000, dtype=bool).reshape(100, 10, order='F'),
    np.random.choice([b'a', b'bb', b'ccc'], size=1000).reshape(10, 10, 10),
    np.random.randint(0, 2**60, size=1000, dtype='u8').view('M8[ns]'),
    np.random.randint(0, 2**60, size=1000, dtype='u8').view('m8[ns]'),
    np.random.randint(0, 2**25, size=1000, dtype='u8').view('M8[m]'),
    np.random.randint(0, 2**25, size=1000, dtype='u8').view('m8[m]'),
]


def test_encode_decode():
    for arr, codec in itertools.product(arrays, codecs):
        check_encode_decode(arr, codec)


def test_config():
    for codec in codecs:
        check_config(codec)


def test_repr():
    check_repr("LZ4(acceleration=1)")
    check_repr("LZ4(acceleration=100)")


def test_backwards_compatibility():
    check_backwards_compatibility(LZ4.codec_id, arrays, codecs)


def test_err_decode_object_buffer():
    check_err_decode_object_buffer(LZ4())


def test_err_encode_object_buffer():
    check_err_encode_object_buffer(LZ4())
