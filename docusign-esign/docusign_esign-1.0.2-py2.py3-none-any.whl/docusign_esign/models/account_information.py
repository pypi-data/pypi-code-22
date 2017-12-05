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


class AccountInformation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, account_id_guid=None, account_name=None, allow_transaction_rooms=None, billing_period_days_remaining=None, billing_period_end_date=None, billing_period_envelopes_allowed=None, billing_period_envelopes_sent=None, billing_period_start_date=None, billing_profile=None, can_cancel_renewal=None, can_upgrade=None, connect_permission=None, created_date=None, currency_code=None, current_plan_id=None, distributor_code=None, docu_sign_landing_url=None, envelope_sending_blocked=None, envelope_unit_price=None, forgotten_password_questions_count=None, is_downgrade=None, payment_method=None, plan_classification=None, plan_end_date=None, plan_name=None, plan_start_date=None, seats_allowed=None, seats_in_use=None, status21_cfr_part11=None, suspension_date=None, suspension_status=None):
        """
        AccountInformation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'account_id_guid': 'str',
            'account_name': 'str',
            'allow_transaction_rooms': 'str',
            'billing_period_days_remaining': 'str',
            'billing_period_end_date': 'str',
            'billing_period_envelopes_allowed': 'str',
            'billing_period_envelopes_sent': 'str',
            'billing_period_start_date': 'str',
            'billing_profile': 'str',
            'can_cancel_renewal': 'str',
            'can_upgrade': 'str',
            'connect_permission': 'str',
            'created_date': 'str',
            'currency_code': 'str',
            'current_plan_id': 'str',
            'distributor_code': 'str',
            'docu_sign_landing_url': 'str',
            'envelope_sending_blocked': 'str',
            'envelope_unit_price': 'str',
            'forgotten_password_questions_count': 'str',
            'is_downgrade': 'str',
            'payment_method': 'str',
            'plan_classification': 'str',
            'plan_end_date': 'str',
            'plan_name': 'str',
            'plan_start_date': 'str',
            'seats_allowed': 'str',
            'seats_in_use': 'str',
            'status21_cfr_part11': 'str',
            'suspension_date': 'str',
            'suspension_status': 'str'
        }

        self.attribute_map = {
            'account_id_guid': 'accountIdGuid',
            'account_name': 'accountName',
            'allow_transaction_rooms': 'allowTransactionRooms',
            'billing_period_days_remaining': 'billingPeriodDaysRemaining',
            'billing_period_end_date': 'billingPeriodEndDate',
            'billing_period_envelopes_allowed': 'billingPeriodEnvelopesAllowed',
            'billing_period_envelopes_sent': 'billingPeriodEnvelopesSent',
            'billing_period_start_date': 'billingPeriodStartDate',
            'billing_profile': 'billingProfile',
            'can_cancel_renewal': 'canCancelRenewal',
            'can_upgrade': 'canUpgrade',
            'connect_permission': 'connectPermission',
            'created_date': 'createdDate',
            'currency_code': 'currencyCode',
            'current_plan_id': 'currentPlanId',
            'distributor_code': 'distributorCode',
            'docu_sign_landing_url': 'docuSignLandingUrl',
            'envelope_sending_blocked': 'envelopeSendingBlocked',
            'envelope_unit_price': 'envelopeUnitPrice',
            'forgotten_password_questions_count': 'forgottenPasswordQuestionsCount',
            'is_downgrade': 'isDowngrade',
            'payment_method': 'paymentMethod',
            'plan_classification': 'planClassification',
            'plan_end_date': 'planEndDate',
            'plan_name': 'planName',
            'plan_start_date': 'planStartDate',
            'seats_allowed': 'seatsAllowed',
            'seats_in_use': 'seatsInUse',
            'status21_cfr_part11': 'status21CFRPart11',
            'suspension_date': 'suspensionDate',
            'suspension_status': 'suspensionStatus'
        }

        self._account_id_guid = account_id_guid
        self._account_name = account_name
        self._allow_transaction_rooms = allow_transaction_rooms
        self._billing_period_days_remaining = billing_period_days_remaining
        self._billing_period_end_date = billing_period_end_date
        self._billing_period_envelopes_allowed = billing_period_envelopes_allowed
        self._billing_period_envelopes_sent = billing_period_envelopes_sent
        self._billing_period_start_date = billing_period_start_date
        self._billing_profile = billing_profile
        self._can_cancel_renewal = can_cancel_renewal
        self._can_upgrade = can_upgrade
        self._connect_permission = connect_permission
        self._created_date = created_date
        self._currency_code = currency_code
        self._current_plan_id = current_plan_id
        self._distributor_code = distributor_code
        self._docu_sign_landing_url = docu_sign_landing_url
        self._envelope_sending_blocked = envelope_sending_blocked
        self._envelope_unit_price = envelope_unit_price
        self._forgotten_password_questions_count = forgotten_password_questions_count
        self._is_downgrade = is_downgrade
        self._payment_method = payment_method
        self._plan_classification = plan_classification
        self._plan_end_date = plan_end_date
        self._plan_name = plan_name
        self._plan_start_date = plan_start_date
        self._seats_allowed = seats_allowed
        self._seats_in_use = seats_in_use
        self._status21_cfr_part11 = status21_cfr_part11
        self._suspension_date = suspension_date
        self._suspension_status = suspension_status

    @property
    def account_id_guid(self):
        """
        Gets the account_id_guid of this AccountInformation.
        The GUID associated with the account ID.

        :return: The account_id_guid of this AccountInformation.
        :rtype: str
        """
        return self._account_id_guid

    @account_id_guid.setter
    def account_id_guid(self, account_id_guid):
        """
        Sets the account_id_guid of this AccountInformation.
        The GUID associated with the account ID.

        :param account_id_guid: The account_id_guid of this AccountInformation.
        :type: str
        """

        self._account_id_guid = account_id_guid

    @property
    def account_name(self):
        """
        Gets the account_name of this AccountInformation.
        The name of the current account.

        :return: The account_name of this AccountInformation.
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """
        Sets the account_name of this AccountInformation.
        The name of the current account.

        :param account_name: The account_name of this AccountInformation.
        :type: str
        """

        self._account_name = account_name

    @property
    def allow_transaction_rooms(self):
        """
        Gets the allow_transaction_rooms of this AccountInformation.
        When set to **true**, the transaction rooms feature exposed through the Workspaces API is enabled.

        :return: The allow_transaction_rooms of this AccountInformation.
        :rtype: str
        """
        return self._allow_transaction_rooms

    @allow_transaction_rooms.setter
    def allow_transaction_rooms(self, allow_transaction_rooms):
        """
        Sets the allow_transaction_rooms of this AccountInformation.
        When set to **true**, the transaction rooms feature exposed through the Workspaces API is enabled.

        :param allow_transaction_rooms: The allow_transaction_rooms of this AccountInformation.
        :type: str
        """

        self._allow_transaction_rooms = allow_transaction_rooms

    @property
    def billing_period_days_remaining(self):
        """
        Gets the billing_period_days_remaining of this AccountInformation.
        Reserved: TBD

        :return: The billing_period_days_remaining of this AccountInformation.
        :rtype: str
        """
        return self._billing_period_days_remaining

    @billing_period_days_remaining.setter
    def billing_period_days_remaining(self, billing_period_days_remaining):
        """
        Sets the billing_period_days_remaining of this AccountInformation.
        Reserved: TBD

        :param billing_period_days_remaining: The billing_period_days_remaining of this AccountInformation.
        :type: str
        """

        self._billing_period_days_remaining = billing_period_days_remaining

    @property
    def billing_period_end_date(self):
        """
        Gets the billing_period_end_date of this AccountInformation.
        Reserved: TBD

        :return: The billing_period_end_date of this AccountInformation.
        :rtype: str
        """
        return self._billing_period_end_date

    @billing_period_end_date.setter
    def billing_period_end_date(self, billing_period_end_date):
        """
        Sets the billing_period_end_date of this AccountInformation.
        Reserved: TBD

        :param billing_period_end_date: The billing_period_end_date of this AccountInformation.
        :type: str
        """

        self._billing_period_end_date = billing_period_end_date

    @property
    def billing_period_envelopes_allowed(self):
        """
        Gets the billing_period_envelopes_allowed of this AccountInformation.
        Reserved: TBD

        :return: The billing_period_envelopes_allowed of this AccountInformation.
        :rtype: str
        """
        return self._billing_period_envelopes_allowed

    @billing_period_envelopes_allowed.setter
    def billing_period_envelopes_allowed(self, billing_period_envelopes_allowed):
        """
        Sets the billing_period_envelopes_allowed of this AccountInformation.
        Reserved: TBD

        :param billing_period_envelopes_allowed: The billing_period_envelopes_allowed of this AccountInformation.
        :type: str
        """

        self._billing_period_envelopes_allowed = billing_period_envelopes_allowed

    @property
    def billing_period_envelopes_sent(self):
        """
        Gets the billing_period_envelopes_sent of this AccountInformation.
        Reserved: TBD

        :return: The billing_period_envelopes_sent of this AccountInformation.
        :rtype: str
        """
        return self._billing_period_envelopes_sent

    @billing_period_envelopes_sent.setter
    def billing_period_envelopes_sent(self, billing_period_envelopes_sent):
        """
        Sets the billing_period_envelopes_sent of this AccountInformation.
        Reserved: TBD

        :param billing_period_envelopes_sent: The billing_period_envelopes_sent of this AccountInformation.
        :type: str
        """

        self._billing_period_envelopes_sent = billing_period_envelopes_sent

    @property
    def billing_period_start_date(self):
        """
        Gets the billing_period_start_date of this AccountInformation.
        Reserved: TBD

        :return: The billing_period_start_date of this AccountInformation.
        :rtype: str
        """
        return self._billing_period_start_date

    @billing_period_start_date.setter
    def billing_period_start_date(self, billing_period_start_date):
        """
        Sets the billing_period_start_date of this AccountInformation.
        Reserved: TBD

        :param billing_period_start_date: The billing_period_start_date of this AccountInformation.
        :type: str
        """

        self._billing_period_start_date = billing_period_start_date

    @property
    def billing_profile(self):
        """
        Gets the billing_profile of this AccountInformation.
        Reserved: TBD

        :return: The billing_profile of this AccountInformation.
        :rtype: str
        """
        return self._billing_profile

    @billing_profile.setter
    def billing_profile(self, billing_profile):
        """
        Sets the billing_profile of this AccountInformation.
        Reserved: TBD

        :param billing_profile: The billing_profile of this AccountInformation.
        :type: str
        """

        self._billing_profile = billing_profile

    @property
    def can_cancel_renewal(self):
        """
        Gets the can_cancel_renewal of this AccountInformation.
        Reserved: TBD

        :return: The can_cancel_renewal of this AccountInformation.
        :rtype: str
        """
        return self._can_cancel_renewal

    @can_cancel_renewal.setter
    def can_cancel_renewal(self, can_cancel_renewal):
        """
        Sets the can_cancel_renewal of this AccountInformation.
        Reserved: TBD

        :param can_cancel_renewal: The can_cancel_renewal of this AccountInformation.
        :type: str
        """

        self._can_cancel_renewal = can_cancel_renewal

    @property
    def can_upgrade(self):
        """
        Gets the can_upgrade of this AccountInformation.
        When set to **true**, specifies that you can upgrade the account through the API.

        :return: The can_upgrade of this AccountInformation.
        :rtype: str
        """
        return self._can_upgrade

    @can_upgrade.setter
    def can_upgrade(self, can_upgrade):
        """
        Sets the can_upgrade of this AccountInformation.
        When set to **true**, specifies that you can upgrade the account through the API.

        :param can_upgrade: The can_upgrade of this AccountInformation.
        :type: str
        """

        self._can_upgrade = can_upgrade

    @property
    def connect_permission(self):
        """
        Gets the connect_permission of this AccountInformation.
        

        :return: The connect_permission of this AccountInformation.
        :rtype: str
        """
        return self._connect_permission

    @connect_permission.setter
    def connect_permission(self, connect_permission):
        """
        Sets the connect_permission of this AccountInformation.
        

        :param connect_permission: The connect_permission of this AccountInformation.
        :type: str
        """

        self._connect_permission = connect_permission

    @property
    def created_date(self):
        """
        Gets the created_date of this AccountInformation.
        

        :return: The created_date of this AccountInformation.
        :rtype: str
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this AccountInformation.
        

        :param created_date: The created_date of this AccountInformation.
        :type: str
        """

        self._created_date = created_date

    @property
    def currency_code(self):
        """
        Gets the currency_code of this AccountInformation.
        Specifies the ISO currency code for the account.

        :return: The currency_code of this AccountInformation.
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """
        Sets the currency_code of this AccountInformation.
        Specifies the ISO currency code for the account.

        :param currency_code: The currency_code of this AccountInformation.
        :type: str
        """

        self._currency_code = currency_code

    @property
    def current_plan_id(self):
        """
        Gets the current_plan_id of this AccountInformation.
        Identifies the plan that was used create this account.

        :return: The current_plan_id of this AccountInformation.
        :rtype: str
        """
        return self._current_plan_id

    @current_plan_id.setter
    def current_plan_id(self, current_plan_id):
        """
        Sets the current_plan_id of this AccountInformation.
        Identifies the plan that was used create this account.

        :param current_plan_id: The current_plan_id of this AccountInformation.
        :type: str
        """

        self._current_plan_id = current_plan_id

    @property
    def distributor_code(self):
        """
        Gets the distributor_code of this AccountInformation.
        The code that identifies the billing plan groups and plans for the new account.

        :return: The distributor_code of this AccountInformation.
        :rtype: str
        """
        return self._distributor_code

    @distributor_code.setter
    def distributor_code(self, distributor_code):
        """
        Sets the distributor_code of this AccountInformation.
        The code that identifies the billing plan groups and plans for the new account.

        :param distributor_code: The distributor_code of this AccountInformation.
        :type: str
        """

        self._distributor_code = distributor_code

    @property
    def docu_sign_landing_url(self):
        """
        Gets the docu_sign_landing_url of this AccountInformation.
        

        :return: The docu_sign_landing_url of this AccountInformation.
        :rtype: str
        """
        return self._docu_sign_landing_url

    @docu_sign_landing_url.setter
    def docu_sign_landing_url(self, docu_sign_landing_url):
        """
        Sets the docu_sign_landing_url of this AccountInformation.
        

        :param docu_sign_landing_url: The docu_sign_landing_url of this AccountInformation.
        :type: str
        """

        self._docu_sign_landing_url = docu_sign_landing_url

    @property
    def envelope_sending_blocked(self):
        """
        Gets the envelope_sending_blocked of this AccountInformation.
        

        :return: The envelope_sending_blocked of this AccountInformation.
        :rtype: str
        """
        return self._envelope_sending_blocked

    @envelope_sending_blocked.setter
    def envelope_sending_blocked(self, envelope_sending_blocked):
        """
        Sets the envelope_sending_blocked of this AccountInformation.
        

        :param envelope_sending_blocked: The envelope_sending_blocked of this AccountInformation.
        :type: str
        """

        self._envelope_sending_blocked = envelope_sending_blocked

    @property
    def envelope_unit_price(self):
        """
        Gets the envelope_unit_price of this AccountInformation.
        

        :return: The envelope_unit_price of this AccountInformation.
        :rtype: str
        """
        return self._envelope_unit_price

    @envelope_unit_price.setter
    def envelope_unit_price(self, envelope_unit_price):
        """
        Sets the envelope_unit_price of this AccountInformation.
        

        :param envelope_unit_price: The envelope_unit_price of this AccountInformation.
        :type: str
        """

        self._envelope_unit_price = envelope_unit_price

    @property
    def forgotten_password_questions_count(self):
        """
        Gets the forgotten_password_questions_count of this AccountInformation.
         A complex element that contains up to four Question/Answer pairs for forgotten password information for a user.

        :return: The forgotten_password_questions_count of this AccountInformation.
        :rtype: str
        """
        return self._forgotten_password_questions_count

    @forgotten_password_questions_count.setter
    def forgotten_password_questions_count(self, forgotten_password_questions_count):
        """
        Sets the forgotten_password_questions_count of this AccountInformation.
         A complex element that contains up to four Question/Answer pairs for forgotten password information for a user.

        :param forgotten_password_questions_count: The forgotten_password_questions_count of this AccountInformation.
        :type: str
        """

        self._forgotten_password_questions_count = forgotten_password_questions_count

    @property
    def is_downgrade(self):
        """
        Gets the is_downgrade of this AccountInformation.
        

        :return: The is_downgrade of this AccountInformation.
        :rtype: str
        """
        return self._is_downgrade

    @is_downgrade.setter
    def is_downgrade(self, is_downgrade):
        """
        Sets the is_downgrade of this AccountInformation.
        

        :param is_downgrade: The is_downgrade of this AccountInformation.
        :type: str
        """

        self._is_downgrade = is_downgrade

    @property
    def payment_method(self):
        """
        Gets the payment_method of this AccountInformation.
        

        :return: The payment_method of this AccountInformation.
        :rtype: str
        """
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        """
        Sets the payment_method of this AccountInformation.
        

        :param payment_method: The payment_method of this AccountInformation.
        :type: str
        """

        self._payment_method = payment_method

    @property
    def plan_classification(self):
        """
        Gets the plan_classification of this AccountInformation.
        Identifies the type of plan. Examples include Business, Corporate, Enterprise, Free.

        :return: The plan_classification of this AccountInformation.
        :rtype: str
        """
        return self._plan_classification

    @plan_classification.setter
    def plan_classification(self, plan_classification):
        """
        Sets the plan_classification of this AccountInformation.
        Identifies the type of plan. Examples include Business, Corporate, Enterprise, Free.

        :param plan_classification: The plan_classification of this AccountInformation.
        :type: str
        """

        self._plan_classification = plan_classification

    @property
    def plan_end_date(self):
        """
        Gets the plan_end_date of this AccountInformation.
        The date that the current plan will end.

        :return: The plan_end_date of this AccountInformation.
        :rtype: str
        """
        return self._plan_end_date

    @plan_end_date.setter
    def plan_end_date(self, plan_end_date):
        """
        Sets the plan_end_date of this AccountInformation.
        The date that the current plan will end.

        :param plan_end_date: The plan_end_date of this AccountInformation.
        :type: str
        """

        self._plan_end_date = plan_end_date

    @property
    def plan_name(self):
        """
        Gets the plan_name of this AccountInformation.
        The name of the Billing Plan.

        :return: The plan_name of this AccountInformation.
        :rtype: str
        """
        return self._plan_name

    @plan_name.setter
    def plan_name(self, plan_name):
        """
        Sets the plan_name of this AccountInformation.
        The name of the Billing Plan.

        :param plan_name: The plan_name of this AccountInformation.
        :type: str
        """

        self._plan_name = plan_name

    @property
    def plan_start_date(self):
        """
        Gets the plan_start_date of this AccountInformation.
        The date that the Account started using the current plan.

        :return: The plan_start_date of this AccountInformation.
        :rtype: str
        """
        return self._plan_start_date

    @plan_start_date.setter
    def plan_start_date(self, plan_start_date):
        """
        Sets the plan_start_date of this AccountInformation.
        The date that the Account started using the current plan.

        :param plan_start_date: The plan_start_date of this AccountInformation.
        :type: str
        """

        self._plan_start_date = plan_start_date

    @property
    def seats_allowed(self):
        """
        Gets the seats_allowed of this AccountInformation.
        

        :return: The seats_allowed of this AccountInformation.
        :rtype: str
        """
        return self._seats_allowed

    @seats_allowed.setter
    def seats_allowed(self, seats_allowed):
        """
        Sets the seats_allowed of this AccountInformation.
        

        :param seats_allowed: The seats_allowed of this AccountInformation.
        :type: str
        """

        self._seats_allowed = seats_allowed

    @property
    def seats_in_use(self):
        """
        Gets the seats_in_use of this AccountInformation.
        

        :return: The seats_in_use of this AccountInformation.
        :rtype: str
        """
        return self._seats_in_use

    @seats_in_use.setter
    def seats_in_use(self, seats_in_use):
        """
        Sets the seats_in_use of this AccountInformation.
        

        :param seats_in_use: The seats_in_use of this AccountInformation.
        :type: str
        """

        self._seats_in_use = seats_in_use

    @property
    def status21_cfr_part11(self):
        """
        Gets the status21_cfr_part11 of this AccountInformation.
        

        :return: The status21_cfr_part11 of this AccountInformation.
        :rtype: str
        """
        return self._status21_cfr_part11

    @status21_cfr_part11.setter
    def status21_cfr_part11(self, status21_cfr_part11):
        """
        Sets the status21_cfr_part11 of this AccountInformation.
        

        :param status21_cfr_part11: The status21_cfr_part11 of this AccountInformation.
        :type: str
        """

        self._status21_cfr_part11 = status21_cfr_part11

    @property
    def suspension_date(self):
        """
        Gets the suspension_date of this AccountInformation.
        

        :return: The suspension_date of this AccountInformation.
        :rtype: str
        """
        return self._suspension_date

    @suspension_date.setter
    def suspension_date(self, suspension_date):
        """
        Sets the suspension_date of this AccountInformation.
        

        :param suspension_date: The suspension_date of this AccountInformation.
        :type: str
        """

        self._suspension_date = suspension_date

    @property
    def suspension_status(self):
        """
        Gets the suspension_status of this AccountInformation.
        

        :return: The suspension_status of this AccountInformation.
        :rtype: str
        """
        return self._suspension_status

    @suspension_status.setter
    def suspension_status(self, suspension_status):
        """
        Sets the suspension_status of this AccountInformation.
        

        :param suspension_status: The suspension_status of this AccountInformation.
        :type: str
        """

        self._suspension_status = suspension_status

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
