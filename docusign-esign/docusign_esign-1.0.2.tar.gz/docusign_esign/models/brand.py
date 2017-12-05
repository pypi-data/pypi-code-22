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


class Brand(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, brand_company=None, brand_id=None, brand_name=None, colors=None, email_content=None, error_details=None, is_overriding_company_name=None, is_sending_default=None, is_signing_default=None, landing_pages=None, links=None, logos=None, resources=None):
        """
        Brand - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'brand_company': 'str',
            'brand_id': 'str',
            'brand_name': 'str',
            'colors': 'list[NameValue]',
            'email_content': 'list[BrandEmailContent]',
            'error_details': 'ErrorDetails',
            'is_overriding_company_name': 'str',
            'is_sending_default': 'str',
            'is_signing_default': 'str',
            'landing_pages': 'list[NameValue]',
            'links': 'list[BrandLink]',
            'logos': 'BrandLogos',
            'resources': 'BrandResourceUrls'
        }

        self.attribute_map = {
            'brand_company': 'brandCompany',
            'brand_id': 'brandId',
            'brand_name': 'brandName',
            'colors': 'colors',
            'email_content': 'emailContent',
            'error_details': 'errorDetails',
            'is_overriding_company_name': 'isOverridingCompanyName',
            'is_sending_default': 'isSendingDefault',
            'is_signing_default': 'isSigningDefault',
            'landing_pages': 'landingPages',
            'links': 'links',
            'logos': 'logos',
            'resources': 'resources'
        }

        self._brand_company = brand_company
        self._brand_id = brand_id
        self._brand_name = brand_name
        self._colors = colors
        self._email_content = email_content
        self._error_details = error_details
        self._is_overriding_company_name = is_overriding_company_name
        self._is_sending_default = is_sending_default
        self._is_signing_default = is_signing_default
        self._landing_pages = landing_pages
        self._links = links
        self._logos = logos
        self._resources = resources

    @property
    def brand_company(self):
        """
        Gets the brand_company of this Brand.
        The name of the company associated with this brand.

        :return: The brand_company of this Brand.
        :rtype: str
        """
        return self._brand_company

    @brand_company.setter
    def brand_company(self, brand_company):
        """
        Sets the brand_company of this Brand.
        The name of the company associated with this brand.

        :param brand_company: The brand_company of this Brand.
        :type: str
        """

        self._brand_company = brand_company

    @property
    def brand_id(self):
        """
        Gets the brand_id of this Brand.
        The ID used to identify a specific brand in API calls.

        :return: The brand_id of this Brand.
        :rtype: str
        """
        return self._brand_id

    @brand_id.setter
    def brand_id(self, brand_id):
        """
        Sets the brand_id of this Brand.
        The ID used to identify a specific brand in API calls.

        :param brand_id: The brand_id of this Brand.
        :type: str
        """

        self._brand_id = brand_id

    @property
    def brand_name(self):
        """
        Gets the brand_name of this Brand.
        The name of the brand.

        :return: The brand_name of this Brand.
        :rtype: str
        """
        return self._brand_name

    @brand_name.setter
    def brand_name(self, brand_name):
        """
        Sets the brand_name of this Brand.
        The name of the brand.

        :param brand_name: The brand_name of this Brand.
        :type: str
        """

        self._brand_name = brand_name

    @property
    def colors(self):
        """
        Gets the colors of this Brand.
        

        :return: The colors of this Brand.
        :rtype: list[NameValue]
        """
        return self._colors

    @colors.setter
    def colors(self, colors):
        """
        Sets the colors of this Brand.
        

        :param colors: The colors of this Brand.
        :type: list[NameValue]
        """

        self._colors = colors

    @property
    def email_content(self):
        """
        Gets the email_content of this Brand.
        

        :return: The email_content of this Brand.
        :rtype: list[BrandEmailContent]
        """
        return self._email_content

    @email_content.setter
    def email_content(self, email_content):
        """
        Sets the email_content of this Brand.
        

        :param email_content: The email_content of this Brand.
        :type: list[BrandEmailContent]
        """

        self._email_content = email_content

    @property
    def error_details(self):
        """
        Gets the error_details of this Brand.

        :return: The error_details of this Brand.
        :rtype: ErrorDetails
        """
        return self._error_details

    @error_details.setter
    def error_details(self, error_details):
        """
        Sets the error_details of this Brand.

        :param error_details: The error_details of this Brand.
        :type: ErrorDetails
        """

        self._error_details = error_details

    @property
    def is_overriding_company_name(self):
        """
        Gets the is_overriding_company_name of this Brand.
        

        :return: The is_overriding_company_name of this Brand.
        :rtype: str
        """
        return self._is_overriding_company_name

    @is_overriding_company_name.setter
    def is_overriding_company_name(self, is_overriding_company_name):
        """
        Sets the is_overriding_company_name of this Brand.
        

        :param is_overriding_company_name: The is_overriding_company_name of this Brand.
        :type: str
        """

        self._is_overriding_company_name = is_overriding_company_name

    @property
    def is_sending_default(self):
        """
        Gets the is_sending_default of this Brand.
        

        :return: The is_sending_default of this Brand.
        :rtype: str
        """
        return self._is_sending_default

    @is_sending_default.setter
    def is_sending_default(self, is_sending_default):
        """
        Sets the is_sending_default of this Brand.
        

        :param is_sending_default: The is_sending_default of this Brand.
        :type: str
        """

        self._is_sending_default = is_sending_default

    @property
    def is_signing_default(self):
        """
        Gets the is_signing_default of this Brand.
        

        :return: The is_signing_default of this Brand.
        :rtype: str
        """
        return self._is_signing_default

    @is_signing_default.setter
    def is_signing_default(self, is_signing_default):
        """
        Sets the is_signing_default of this Brand.
        

        :param is_signing_default: The is_signing_default of this Brand.
        :type: str
        """

        self._is_signing_default = is_signing_default

    @property
    def landing_pages(self):
        """
        Gets the landing_pages of this Brand.
        

        :return: The landing_pages of this Brand.
        :rtype: list[NameValue]
        """
        return self._landing_pages

    @landing_pages.setter
    def landing_pages(self, landing_pages):
        """
        Sets the landing_pages of this Brand.
        

        :param landing_pages: The landing_pages of this Brand.
        :type: list[NameValue]
        """

        self._landing_pages = landing_pages

    @property
    def links(self):
        """
        Gets the links of this Brand.
        

        :return: The links of this Brand.
        :rtype: list[BrandLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this Brand.
        

        :param links: The links of this Brand.
        :type: list[BrandLink]
        """

        self._links = links

    @property
    def logos(self):
        """
        Gets the logos of this Brand.

        :return: The logos of this Brand.
        :rtype: BrandLogos
        """
        return self._logos

    @logos.setter
    def logos(self, logos):
        """
        Sets the logos of this Brand.

        :param logos: The logos of this Brand.
        :type: BrandLogos
        """

        self._logos = logos

    @property
    def resources(self):
        """
        Gets the resources of this Brand.

        :return: The resources of this Brand.
        :rtype: BrandResourceUrls
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this Brand.

        :param resources: The resources of this Brand.
        :type: BrandResourceUrls
        """

        self._resources = resources

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
