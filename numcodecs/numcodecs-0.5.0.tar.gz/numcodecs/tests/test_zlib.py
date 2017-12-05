# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division
import itertools


import numpy as np
from nose.tools import eq_ as eq


from numcodecs.zlib import Zlib
from numcodecs.registry import get_codec
from numcodecs.tests.common import (check_encode_decode, check_config, check_repr,
                                    check_backwards_compatibility,
                                    check_err_decode_object_buffer,
                                    check_err_encode_object_buffer)


codecs = [
    Zlib(),
    Zlib(level=-1),
    Zlib(level=0),
    Zlib(level=1),
    Zlib(level=5),
    Zlib(level=9),
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
    codec = Zlib(level=3)
    check_config(codec)


def test_repr():
    check_repr("Zlib(level=3)")


def test_alias():
    config = dict(id='gzip', level=1)
    codec = get_codec(config)
    eq(Zlib(1), codec)


def test_eq():
    assert Zlib() == Zlib()
    assert not Zlib() != Zlib()
    assert Zlib(1) == Zlib(1)
    assert Zlib(1) != Zlib(9)
    assert Zlib() != 'foo'
    assert 'foo' != Zlib()
    assert not Zlib() == 'foo'


def test_backwards_compatibility():
    check_backwards_compatibility(Zlib.codec_id, arrays, codecs)


def test_err_decode_object_buffer():
    check_err_decode_object_buffer(Zlib())


def test_err_encode_object_buffer():
    check_err_encode_object_buffer(Zlib())
