# coding: utf-8

"""
    DocuSign REST API

    The DocuSign REST API provides you with a powerful, convenient, and simple Web services API for interacting with DocuSign.

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SeatDiscount(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, begin_seat_count=None, discount_percent=None, end_seat_count=None):
        """
        SeatDiscount - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'begin_seat_count': 'str',
            'discount_percent': 'str',
            'end_seat_count': 'str'
        }

        self.attribute_map = {
            'begin_seat_count': 'beginSeatCount',
            'discount_percent': 'discountPercent',
            'end_seat_count': 'endSeatCount'
        }

        self._begin_seat_count = begin_seat_count
        self._discount_percent = discount_percent
        self._end_seat_count = end_seat_count

    @property
    def begin_seat_count(self):
        """
        Gets the begin_seat_count of this SeatDiscount.
        Reserved: TBD

        :return: The begin_seat_count of this SeatDiscount.
        :rtype: str
        """
        return self._begin_seat_count

    @begin_seat_count.setter
    def begin_seat_count(self, begin_seat_count):
        """
        Sets the begin_seat_count of this SeatDiscount.
        Reserved: TBD

        :param begin_seat_count: The begin_seat_count of this SeatDiscount.
        :type: str
        """

        self._begin_seat_count = begin_seat_count

    @property
    def discount_percent(self):
        """
        Gets the discount_percent of this SeatDiscount.
        

        :return: The discount_percent of this SeatDiscount.
        :rtype: str
        """
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, discount_percent):
        """
        Sets the discount_percent of this SeatDiscount.
        

        :param discount_percent: The discount_percent of this SeatDiscount.
        :type: str
        """

        self._discount_percent = discount_percent

    @property
    def end_seat_count(self):
        """
        Gets the end_seat_count of this SeatDiscount.
        Reserved: TBD

        :return: The end_seat_count of this SeatDiscount.
        :rtype: str
        """
        return self._end_seat_count

    @end_seat_count.setter
    def end_seat_count(self, end_seat_count):
        """
        Sets the end_seat_count of this SeatDiscount.
        Reserved: TBD

        :param end_seat_count: The end_seat_count of this SeatDiscount.
        :type: str
        """

        self._end_seat_count = end_seat_count

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
