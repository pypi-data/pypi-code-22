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


class EnvelopeSummary(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, envelope_id=None, status=None, status_date_time=None, uri=None):
        """
        EnvelopeSummary - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'envelope_id': 'str',
            'status': 'str',
            'status_date_time': 'str',
            'uri': 'str'
        }

        self.attribute_map = {
            'envelope_id': 'envelopeId',
            'status': 'status',
            'status_date_time': 'statusDateTime',
            'uri': 'uri'
        }

        self._envelope_id = envelope_id
        self._status = status
        self._status_date_time = status_date_time
        self._uri = uri

    @property
    def envelope_id(self):
        """
        Gets the envelope_id of this EnvelopeSummary.
        The envelope ID of the envelope status that failed to post.

        :return: The envelope_id of this EnvelopeSummary.
        :rtype: str
        """
        return self._envelope_id

    @envelope_id.setter
    def envelope_id(self, envelope_id):
        """
        Sets the envelope_id of this EnvelopeSummary.
        The envelope ID of the envelope status that failed to post.

        :param envelope_id: The envelope_id of this EnvelopeSummary.
        :type: str
        """

        self._envelope_id = envelope_id

    @property
    def status(self):
        """
        Gets the status of this EnvelopeSummary.
        Indicates the envelope status. Valid values are:  * sent - The envelope is sent to the recipients.  * created - The envelope is saved as a draft and can be modified and sent later.

        :return: The status of this EnvelopeSummary.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this EnvelopeSummary.
        Indicates the envelope status. Valid values are:  * sent - The envelope is sent to the recipients.  * created - The envelope is saved as a draft and can be modified and sent later.

        :param status: The status of this EnvelopeSummary.
        :type: str
        """

        self._status = status

    @property
    def status_date_time(self):
        """
        Gets the status_date_time of this EnvelopeSummary.
        The DateTime that the envelope changed status (i.e. was created or sent.)

        :return: The status_date_time of this EnvelopeSummary.
        :rtype: str
        """
        return self._status_date_time

    @status_date_time.setter
    def status_date_time(self, status_date_time):
        """
        Sets the status_date_time of this EnvelopeSummary.
        The DateTime that the envelope changed status (i.e. was created or sent.)

        :param status_date_time: The status_date_time of this EnvelopeSummary.
        :type: str
        """

        self._status_date_time = status_date_time

    @property
    def uri(self):
        """
        Gets the uri of this EnvelopeSummary.
        

        :return: The uri of this EnvelopeSummary.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this EnvelopeSummary.
        

        :param uri: The uri of this EnvelopeSummary.
        :type: str
        """

        self._uri = uri

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
