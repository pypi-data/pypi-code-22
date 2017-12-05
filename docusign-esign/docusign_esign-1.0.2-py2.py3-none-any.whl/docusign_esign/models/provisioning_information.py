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


class ProvisioningInformation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, default_connection_id=None, default_plan_id=None, distributor_code=None, distributor_password=None, password_rule_text=None, plan_promotion_text=None, purchase_order_or_prom_allowed=None):
        """
        ProvisioningInformation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'default_connection_id': 'str',
            'default_plan_id': 'str',
            'distributor_code': 'str',
            'distributor_password': 'str',
            'password_rule_text': 'str',
            'plan_promotion_text': 'str',
            'purchase_order_or_prom_allowed': 'str'
        }

        self.attribute_map = {
            'default_connection_id': 'defaultConnectionId',
            'default_plan_id': 'defaultPlanId',
            'distributor_code': 'distributorCode',
            'distributor_password': 'distributorPassword',
            'password_rule_text': 'passwordRuleText',
            'plan_promotion_text': 'planPromotionText',
            'purchase_order_or_prom_allowed': 'purchaseOrderOrPromAllowed'
        }

        self._default_connection_id = default_connection_id
        self._default_plan_id = default_plan_id
        self._distributor_code = distributor_code
        self._distributor_password = distributor_password
        self._password_rule_text = password_rule_text
        self._plan_promotion_text = plan_promotion_text
        self._purchase_order_or_prom_allowed = purchase_order_or_prom_allowed

    @property
    def default_connection_id(self):
        """
        Gets the default_connection_id of this ProvisioningInformation.
        

        :return: The default_connection_id of this ProvisioningInformation.
        :rtype: str
        """
        return self._default_connection_id

    @default_connection_id.setter
    def default_connection_id(self, default_connection_id):
        """
        Sets the default_connection_id of this ProvisioningInformation.
        

        :param default_connection_id: The default_connection_id of this ProvisioningInformation.
        :type: str
        """

        self._default_connection_id = default_connection_id

    @property
    def default_plan_id(self):
        """
        Gets the default_plan_id of this ProvisioningInformation.
        

        :return: The default_plan_id of this ProvisioningInformation.
        :rtype: str
        """
        return self._default_plan_id

    @default_plan_id.setter
    def default_plan_id(self, default_plan_id):
        """
        Sets the default_plan_id of this ProvisioningInformation.
        

        :param default_plan_id: The default_plan_id of this ProvisioningInformation.
        :type: str
        """

        self._default_plan_id = default_plan_id

    @property
    def distributor_code(self):
        """
        Gets the distributor_code of this ProvisioningInformation.
        The code that identifies the billing plan groups and plans for the new account.

        :return: The distributor_code of this ProvisioningInformation.
        :rtype: str
        """
        return self._distributor_code

    @distributor_code.setter
    def distributor_code(self, distributor_code):
        """
        Sets the distributor_code of this ProvisioningInformation.
        The code that identifies the billing plan groups and plans for the new account.

        :param distributor_code: The distributor_code of this ProvisioningInformation.
        :type: str
        """

        self._distributor_code = distributor_code

    @property
    def distributor_password(self):
        """
        Gets the distributor_password of this ProvisioningInformation.
        The password for the distributorCode.

        :return: The distributor_password of this ProvisioningInformation.
        :rtype: str
        """
        return self._distributor_password

    @distributor_password.setter
    def distributor_password(self, distributor_password):
        """
        Sets the distributor_password of this ProvisioningInformation.
        The password for the distributorCode.

        :param distributor_password: The distributor_password of this ProvisioningInformation.
        :type: str
        """

        self._distributor_password = distributor_password

    @property
    def password_rule_text(self):
        """
        Gets the password_rule_text of this ProvisioningInformation.
        

        :return: The password_rule_text of this ProvisioningInformation.
        :rtype: str
        """
        return self._password_rule_text

    @password_rule_text.setter
    def password_rule_text(self, password_rule_text):
        """
        Sets the password_rule_text of this ProvisioningInformation.
        

        :param password_rule_text: The password_rule_text of this ProvisioningInformation.
        :type: str
        """

        self._password_rule_text = password_rule_text

    @property
    def plan_promotion_text(self):
        """
        Gets the plan_promotion_text of this ProvisioningInformation.
        

        :return: The plan_promotion_text of this ProvisioningInformation.
        :rtype: str
        """
        return self._plan_promotion_text

    @plan_promotion_text.setter
    def plan_promotion_text(self, plan_promotion_text):
        """
        Sets the plan_promotion_text of this ProvisioningInformation.
        

        :param plan_promotion_text: The plan_promotion_text of this ProvisioningInformation.
        :type: str
        """

        self._plan_promotion_text = plan_promotion_text

    @property
    def purchase_order_or_prom_allowed(self):
        """
        Gets the purchase_order_or_prom_allowed of this ProvisioningInformation.
        

        :return: The purchase_order_or_prom_allowed of this ProvisioningInformation.
        :rtype: str
        """
        return self._purchase_order_or_prom_allowed

    @purchase_order_or_prom_allowed.setter
    def purchase_order_or_prom_allowed(self, purchase_order_or_prom_allowed):
        """
        Sets the purchase_order_or_prom_allowed of this ProvisioningInformation.
        

        :param purchase_order_or_prom_allowed: The purchase_order_or_prom_allowed of this ProvisioningInformation.
        :type: str
        """

        self._purchase_order_or_prom_allowed = purchase_order_or_prom_allowed

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
