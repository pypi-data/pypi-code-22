# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime, time
from decimal import Decimal

import pytest
import six

from mariadb_dyncol import DynColLimitError, DynColNotSupported, DynColTypeError, DynColValueError, pack, unpack
from mariadb_dyncol.base import MAX_NAME_LENGTH  # private but useful in tests

from .base import check, hexs, unhexs


def test_empty():
    check({}, b"0400000000")


def test_a_1():
    check({"a": 1}, b"0401000100000000006102")


def test_a_minus1():
    check({"a": -1}, b"0401000100000000006101")


def test_a_minus2():
    check({"a": -2}, b"0401000100000000006103")


def test_a_0():
    check({"a": 0}, b"04010001000000000061")


def test_a_128():
    check({"a": 128}, b"040100010000000000610001")


def test_a_65535():
    check({"a": 65535}, b"04010001000000000061feff01")


def test_a_1048576():
    check({"a": 1048576}, b"04010001000000000061000020")


def test_0_2147483648():
    check({'0': 2147483648}, b'040100010000000000300000000001')


def test_ulonglongmax():
    check(
        {"a": 18446744073709551615},
        b"04010001000000010061ffffffffffffffff"
    )


def test_integer_overflow():
    with pytest.raises(DynColValueError):
        check({"a": 2 ** 64}, b"unchecked")


def test_integer_negative_overflow():
    with pytest.raises(DynColValueError):
        check({"a": -(2 ** 32)}, b"unchecked")


def test_c_1():
    check({"c": 1}, b"0401000100000000006302")


def test_a_1_b_2():
    check({"a": 1, "b": 2}, b"0402000200000000000100100061620204")


def test_a_1_b_2_c_3():
    check(
        {"a": 1, "b": 2, "c": 3},
        b"0403000300000000000100100002002000616263020406"
    )


def test_abc_123():
    check({"abc": 123}, b"040100030000000000616263f6")


def test_string_empty():
    check({"a": ""}, b"0401000100000003006121")


def test_empty_key():
    check({"": ""}, b"04010000000000030021")


def test_string_values():
    check({"a": "string"}, b"0401000100000003006121737472696e67")


def test_a_unicode_poo():
    check({"a": "💩"}, b"0401000100000003006121f09f92a9")


def test_unicode_poo_1():
    check({"💩": 1}, b"040100040000000000f09f92a902")


def test_unicode_utf8mb4_unpack():
    # All tests are using utf8 on connection but we should recognize utf8mb4
    # as well
    assert unpack(unhexs('040100010000000300612d61')) == {"a": "a"}


def test_non_unicode_charset_fails():
    with pytest.raises(DynColNotSupported):
        unpack(unhexs('040100010000000300610861'))  # {'a': 'a'} in latin1


@pytest.mark.skipif(not six.PY2, reason="requires Python 2")
def test_str_not_accepted():
    with pytest.raises(DynColTypeError):
        pack({'a': str('value')})


@pytest.mark.slow
def test_large_string_data_4093_as():
    check(
        {'a': 'a' * 4093},
        b'0401000100000003006121616161',
        hexstring_cut=True
    )


@pytest.mark.slow
def test_large_string_data_4094_as():
    check(
        {'a': 'a' * 4094},
        b'050100010000000300006121616161',
        hexstring_cut=True
    )


@pytest.mark.slow
def test_large_string_data_4095_as():
    check(
        {'a': 'a' * 4095},
        b'050100010000000300006121616161',
        hexstring_cut=True
    )


@pytest.mark.slow
def test_large_string_data_4096_as():
    check(
        {'a': 'a' * 4096},
        b'050100010000000300006121616161',
        hexstring_cut=True
    )


@pytest.mark.slow
def test_large_string_data_2():
    check(
        {'a': 'a' * (2 ** 13), 'b': 1},
        b'0502000200000003000001001000026162216161',
        hexstring_cut=True
    )


@pytest.mark.slow
def test_huge_string_data():
    check(
        {'a': 'a' * (2 ** 20)},
        b'06010001000000030000006121616161',
        hexstring_cut=True
    )


def test_None():
    check({"a": None}, b"0400000000")


def test_dict():
    check(
        {"a": {"b": "c"}},
        b"04010001000000080061040100010000000300622163"
    )


def test_float_1_0():
    check({"a": 1.0}, b"04010001000000020061000000000000f03f")


def test_float_minus_3_415():
    check({"a": -3.415}, b"0401000100000002006152b81e85eb510bc0")


def test_float_minus_0_0():
    # MariaDB is discards the minus sign
    check({"0": -0.0}, b"040100010000000200300000000000000000")


def test_float_192873409809():
    check(
        {"a": 192873409809.0},
        b"040100010000000200610080885613744642"
    )


def test_float_1000000000000001():
    check(
        {'0': 1000000000000001.0},
        b'0401000100000002003008003426f56b0c43'
    )


def test_float_nan_not_stored():
    with pytest.raises(DynColValueError):
        pack({"a": float('nan')})


def test_float_inf_not_stored():
    with pytest.raises(DynColValueError):
        pack({"a": float('inf')})


def test_pack_Decimal_not_implemented():
    with pytest.raises(DynColNotSupported):
        pack({'a': Decimal(1)})


def test_unpack_Decimal_not_implemented():
    with pytest.raises(DynColNotSupported):
        # Contains Decimal 1
        unpack(unhexs(b'04010001000000040061090080000001'))


# def test_decimal_1():
#     check({'a': Decimal('1')}, b'04010001000000040061090080000001')


# def test_decimal_123456789():
#     check({'a': Decimal('123456789')}, b'040100010000000400610900875bcd15')


# def test_decimal_123456789_5():
#     check({'a': Decimal('123456789.5')},
#            b'040100010000000400610901875bcd1505')


def test_datetime():
    check(
        {"a": datetime(year=1989, month=10, day=4,
                       hour=3, minute=4, second=55, microsecond=142859)},
        b"04010001000000050061448b0f0b2e72130300"
    )


def test_datetime_2():
    check(
        {"a": datetime(year=2300, month=12, day=25,
                       hour=15, minute=55, second=12, microsecond=998134)},
        b"0401000100000005006199f911f63acfdc0f00"
    )


def test_datetime_no_microseconds():
    check(
        {"0": datetime(year=2000, month=1, day=1,
                       hour=0, minute=0, second=0)},
        b"0401000100000005003021a00f000000"
    )


def test_date():
    check(
        {"a": date(year=2015, month=1, day=1)},
        b"0401000100000006006121be0f"
    )


def test_date_2():
    check(
        {"a": date(year=1, month=12, day=25)},
        b"04010001000000060061990300"
    )


def test_time():
    check(
        {"a": time(hour=12, minute=2, second=3, microsecond=676767)},
        b"040100010000000700619f533a080c00"
    )


def test_time_2():
    check(
        {"a": time(hour=3, minute=59, second=59, microsecond=999999)},
        b"040100010000000700613f42bfef0300"
    )


def test_time_no_microseconds():
    check(
        {"a": time(hour=1, minute=2, second=3)},
        b"04010001000000070061831000"
    )


def test_cyrillic_key():
    check(
        {'адын': 1212},
        b'040100080000000000d0b0d0b4d18bd0bd7809'
    )


def test_1212_1212():
    check(
        {"1212": 1212},
        b'040100040000000000313231327809'
    )


def test_two_keys():
    check(
        {"1212": 2, "www": 3},
        b'04020007000000000003001000777777313231320604',
    )


def test_two_keys_other():
    check(
        {"1": "AAA", "b": "BBB"},
        b'0402000200000003000100430031622141414121424242',
    )


def test_255_chars():
    check(
        {'a' * 255: 1},
        b'040100ff0000000000' + b''.join([b'61'] * 255) + b'02'
    )


def test_000_negative_lowest():
    check(
        {'000': -2147483647, '0\x80': -2147483647},
        b'0402000600000000000300400030303030c280fdfffffffdffffff'
    )


def test_MAX_NAME_LENGTH_chars():
    long_key = 'a' * MAX_NAME_LENGTH
    long_key_encoded = long_key.encode('utf-8')
    check(
        {long_key: 1},
        b'040100ff3f00000000' + hexs(long_key_encoded) + b'02'
    )


def test_name_overflow():
    with pytest.raises(DynColLimitError):
        pack({'a' * (MAX_NAME_LENGTH + 1): 1})


def test_name_unicode_fits():
    long_key = ('💩' * 4095) + ('a' * 3)  # MAX_NAME_LENGTH bytes
    long_key_encoded = long_key.encode('utf8')
    check(
        {long_key: 1},
        b'040100ff3f00000000' + hexs(long_key_encoded) + b'02'
    )


def test_name_unicode_overflow():
    long_key = ('💩' * 4095) + ('a' * 4)  # MAX_NAME_LENGTH + 1 bytes
    with pytest.raises(DynColLimitError):
        pack({long_key: 1})


def test_total_name_length():
    long_key = 'a' * (MAX_NAME_LENGTH - 1)
    # No exception
    pack({
        long_key + '1': 1,
        long_key + '2': 1,
        long_key + '3': 1,
        long_key + '4': 1,
        'abc': 1    # Total up to here = TOTAL_MAX_NAME_LENGTH
    })


def test_total_name_length_overflow():
    long_key = 'a' * (MAX_NAME_LENGTH - 1)
    with pytest.raises(DynColLimitError):
        pack({
            long_key + '1': 1,
            long_key + '2': 1,
            long_key + '3': 1,
            long_key + '4': 1,
            'abc': 1,  # Total up to here = TOTAL_MAX_NAME_LENGTH
            'a': 1,
        })


def test_nested():
    check(
        {'falafel': {'a': 1}, 'fala': {'b': 't'}},
        b'0402000b00000008000400c80066616c6166616c6166656c040100010000000'
        b'3006221740401000100000000006102'
    )


def test_nested_empty():
    check(
        {'0': {}},
        b'040100010000000800300400000000'
    )


def test_unknown_type():
    with pytest.raises(DynColTypeError):
        pack({'key': ['lists', 'not', 'supported']})


def test_unknown_columns_format():
    with pytest.raises(DynColValueError):
        # Numbered columns format as pulled from MariaDB tests
        unpack(b'0001000100030861666166')
