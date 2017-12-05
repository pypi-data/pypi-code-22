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


class SignatureProviderRequiredOption(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, required_signature_provider_option_ids=None, signer_type=None):
        """
        SignatureProviderRequiredOption - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'required_signature_provider_option_ids': 'list[str]',
            'signer_type': 'str'
        }

        self.attribute_map = {
            'required_signature_provider_option_ids': 'requiredSignatureProviderOptionIds',
            'signer_type': 'signerType'
        }

        self._required_signature_provider_option_ids = required_signature_provider_option_ids
        self._signer_type = signer_type

    @property
    def required_signature_provider_option_ids(self):
        """
        Gets the required_signature_provider_option_ids of this SignatureProviderRequiredOption.
        

        :return: The required_signature_provider_option_ids of this SignatureProviderRequiredOption.
        :rtype: list[str]
        """
        return self._required_signature_provider_option_ids

    @required_signature_provider_option_ids.setter
    def required_signature_provider_option_ids(self, required_signature_provider_option_ids):
        """
        Sets the required_signature_provider_option_ids of this SignatureProviderRequiredOption.
        

        :param required_signature_provider_option_ids: The required_signature_provider_option_ids of this SignatureProviderRequiredOption.
        :type: list[str]
        """

        self._required_signature_provider_option_ids = required_signature_provider_option_ids

    @property
    def signer_type(self):
        """
        Gets the signer_type of this SignatureProviderRequiredOption.
        

        :return: The signer_type of this SignatureProviderRequiredOption.
        :rtype: str
        """
        return self._signer_type

    @signer_type.setter
    def signer_type(self, signer_type):
        """
        Sets the signer_type of this SignatureProviderRequiredOption.
        

        :param signer_type: The signer_type of this SignatureProviderRequiredOption.
        :type: str
        """

        self._signer_type = signer_type

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
