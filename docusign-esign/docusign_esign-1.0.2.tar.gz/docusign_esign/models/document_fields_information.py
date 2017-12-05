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


class DocumentFieldsInformation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, document_fields=None):
        """
        DocumentFieldsInformation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'document_fields': 'list[NameValue]'
        }

        self.attribute_map = {
            'document_fields': 'documentFields'
        }

        self._document_fields = document_fields

    @property
    def document_fields(self):
        """
        Gets the document_fields of this DocumentFieldsInformation.
        The array of name/value custom data strings to be added to a document. Custom document field information is returned in the status, but otherwise is not used by DocuSign. The array contains the elements:   * name – A string that can be a maximum of 50 characters.  * value – A string that can be a maximum of 200 characters.  *IMPORTANT*: If you are using xml, the name/value pair is contained in a nameValue element.  

        :return: The document_fields of this DocumentFieldsInformation.
        :rtype: list[NameValue]
        """
        return self._document_fields

    @document_fields.setter
    def document_fields(self, document_fields):
        """
        Sets the document_fields of this DocumentFieldsInformation.
        The array of name/value custom data strings to be added to a document. Custom document field information is returned in the status, but otherwise is not used by DocuSign. The array contains the elements:   * name – A string that can be a maximum of 50 characters.  * value – A string that can be a maximum of 200 characters.  *IMPORTANT*: If you are using xml, the name/value pair is contained in a nameValue element.  

        :param document_fields: The document_fields of this DocumentFieldsInformation.
        :type: list[NameValue]
        """

        self._document_fields = document_fields

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
