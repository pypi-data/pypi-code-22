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


class CaptiveRecipient(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, client_user_id=None, email=None, error_details=None, user_name=None):
        """
        CaptiveRecipient - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'client_user_id': 'str',
            'email': 'str',
            'error_details': 'ErrorDetails',
            'user_name': 'str'
        }

        self.attribute_map = {
            'client_user_id': 'clientUserId',
            'email': 'email',
            'error_details': 'errorDetails',
            'user_name': 'userName'
        }

        self._client_user_id = client_user_id
        self._email = email
        self._error_details = error_details
        self._user_name = user_name

    @property
    def client_user_id(self):
        """
        Gets the client_user_id of this CaptiveRecipient.
        Specifies whether the recipient is embedded or remote.   If the `clientUserId` property is not null then the recipient is embedded. Note that if the `ClientUserId` property is set and either `SignerMustHaveAccount` or `SignerMustLoginToSign` property of the account settings is set to  **true**, an error is generated on sending.ng.   Maximum length: 100 characters. 

        :return: The client_user_id of this CaptiveRecipient.
        :rtype: str
        """
        return self._client_user_id

    @client_user_id.setter
    def client_user_id(self, client_user_id):
        """
        Sets the client_user_id of this CaptiveRecipient.
        Specifies whether the recipient is embedded or remote.   If the `clientUserId` property is not null then the recipient is embedded. Note that if the `ClientUserId` property is set and either `SignerMustHaveAccount` or `SignerMustLoginToSign` property of the account settings is set to  **true**, an error is generated on sending.ng.   Maximum length: 100 characters. 

        :param client_user_id: The client_user_id of this CaptiveRecipient.
        :type: str
        """

        self._client_user_id = client_user_id

    @property
    def email(self):
        """
        Gets the email of this CaptiveRecipient.
        Specifies the email address associated with the captive recipient.

        :return: The email of this CaptiveRecipient.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this CaptiveRecipient.
        Specifies the email address associated with the captive recipient.

        :param email: The email of this CaptiveRecipient.
        :type: str
        """

        self._email = email

    @property
    def error_details(self):
        """
        Gets the error_details of this CaptiveRecipient.

        :return: The error_details of this CaptiveRecipient.
        :rtype: ErrorDetails
        """
        return self._error_details

    @error_details.setter
    def error_details(self, error_details):
        """
        Sets the error_details of this CaptiveRecipient.

        :param error_details: The error_details of this CaptiveRecipient.
        :type: ErrorDetails
        """

        self._error_details = error_details

    @property
    def user_name(self):
        """
        Gets the user_name of this CaptiveRecipient.
        Specifies the user name associated with the captive recipient.

        :return: The user_name of this CaptiveRecipient.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this CaptiveRecipient.
        Specifies the user name associated with the captive recipient.

        :param user_name: The user_name of this CaptiveRecipient.
        :type: str
        """

        self._user_name = user_name

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
