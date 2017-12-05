# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np
import nose
from nose.tools import assert_raises


try:
    from numcodecs.vlen import VLenUTF8
except ImportError:  # pragma: no cover
    raise nose.SkipTest("vlen-utf8 not available")
from numcodecs.tests.common import (check_config, check_repr, check_encode_decode_array,
                                    check_backwards_compatibility, greetings)


arrays = [
    np.array([u'foo', u'bar', u'baz'] * 300, dtype=object),
    np.array(greetings * 100, dtype=object),
    np.array([u'foo', u'bar', u'baz'] * 300, dtype=object).reshape(90, 10),
    np.array(greetings * 1000, dtype=object).reshape(len(greetings), 100, 10, order='F'),
]


def test_encode_decode():
    for arr in arrays:
        codec = VLenUTF8()
        check_encode_decode_array(arr, codec)


def test_config():
    codec = VLenUTF8()
    check_config(codec)


def test_repr():
    check_repr("VLenUTF8()")


def test_backwards_compatibility():
    check_backwards_compatibility(VLenUTF8.codec_id, arrays, [VLenUTF8()])


def test_encode_errors():
    codec = VLenUTF8()
    with assert_raises(TypeError):
        codec.encode(1234)
    with assert_raises(TypeError):
        codec.encode([1234, 5678])
    with assert_raises(TypeError):
        codec.encode(np.zeros(10, dtype='i4'))


def test_decode_errors():
    codec = VLenUTF8()
    with assert_raises(TypeError):
        codec.decode(u'foo')
    with assert_raises(TypeError):
        codec.decode(1234)
    # these should look like corrupt data
    with assert_raises(ValueError):
        codec.decode(b'foo')
    with assert_raises(ValueError):
        codec.decode(np.arange(2, 3, dtype='i4'))
    with assert_raises(ValueError):
        codec.decode(np.arange(10, 20, dtype='i4'))

    # test out parameter
    enc = codec.encode(arrays[0])
    with assert_raises(TypeError):
        codec.decode(enc, out=b'foo')
    with assert_raises(TypeError):
        codec.decode(enc, out=u'foo')
    with assert_raises(TypeError):
        codec.decode(enc, out=123)
    with assert_raises(ValueError):
        codec.decode(enc, out=np.zeros(10, dtype='i4'))
