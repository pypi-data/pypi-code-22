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


class BulkRecipientsRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, bulk_recipients=None):
        """
        BulkRecipientsRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'bulk_recipients': 'list[BulkRecipient]'
        }

        self.attribute_map = {
            'bulk_recipients': 'bulkRecipients'
        }

        self._bulk_recipients = bulk_recipients

    @property
    def bulk_recipients(self):
        """
        Gets the bulk_recipients of this BulkRecipientsRequest.
        A complex type containing information about the bulk recipients in the request.

        :return: The bulk_recipients of this BulkRecipientsRequest.
        :rtype: list[BulkRecipient]
        """
        return self._bulk_recipients

    @bulk_recipients.setter
    def bulk_recipients(self, bulk_recipients):
        """
        Sets the bulk_recipients of this BulkRecipientsRequest.
        A complex type containing information about the bulk recipients in the request.

        :param bulk_recipients: The bulk_recipients of this BulkRecipientsRequest.
        :type: list[BulkRecipient]
        """

        self._bulk_recipients = bulk_recipients

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
