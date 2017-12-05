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


class TemplateRole(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, access_code=None, client_user_id=None, default_recipient=None, email=None, email_notification=None, embedded_recipient_start_url=None, in_person_signer_name=None, name=None, recipient_signature_providers=None, role_name=None, routing_order=None, signing_group_id=None, tabs=None):
        """
        TemplateRole - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'access_code': 'str',
            'client_user_id': 'str',
            'default_recipient': 'str',
            'email': 'str',
            'email_notification': 'RecipientEmailNotification',
            'embedded_recipient_start_url': 'str',
            'in_person_signer_name': 'str',
            'name': 'str',
            'recipient_signature_providers': 'list[RecipientSignatureProvider]',
            'role_name': 'str',
            'routing_order': 'str',
            'signing_group_id': 'str',
            'tabs': 'Tabs'
        }

        self.attribute_map = {
            'access_code': 'accessCode',
            'client_user_id': 'clientUserId',
            'default_recipient': 'defaultRecipient',
            'email': 'email',
            'email_notification': 'emailNotification',
            'embedded_recipient_start_url': 'embeddedRecipientStartURL',
            'in_person_signer_name': 'inPersonSignerName',
            'name': 'name',
            'recipient_signature_providers': 'recipientSignatureProviders',
            'role_name': 'roleName',
            'routing_order': 'routingOrder',
            'signing_group_id': 'signingGroupId',
            'tabs': 'tabs'
        }

        self._access_code = access_code
        self._client_user_id = client_user_id
        self._default_recipient = default_recipient
        self._email = email
        self._email_notification = email_notification
        self._embedded_recipient_start_url = embedded_recipient_start_url
        self._in_person_signer_name = in_person_signer_name
        self._name = name
        self._recipient_signature_providers = recipient_signature_providers
        self._role_name = role_name
        self._routing_order = routing_order
        self._signing_group_id = signing_group_id
        self._tabs = tabs

    @property
    def access_code(self):
        """
        Gets the access_code of this TemplateRole.
        If a value is provided, the recipient must enter the value as the access code to view and sign the envelope.   Maximum Length: 50 characters and it must conform to the account’s access code format setting.  If blank, but the signer `accessCode` property is set in the envelope, then that value is used.  If blank and the signer `accessCode` property is not set, then the access code is not required.

        :return: The access_code of this TemplateRole.
        :rtype: str
        """
        return self._access_code

    @access_code.setter
    def access_code(self, access_code):
        """
        Sets the access_code of this TemplateRole.
        If a value is provided, the recipient must enter the value as the access code to view and sign the envelope.   Maximum Length: 50 characters and it must conform to the account’s access code format setting.  If blank, but the signer `accessCode` property is set in the envelope, then that value is used.  If blank and the signer `accessCode` property is not set, then the access code is not required.

        :param access_code: The access_code of this TemplateRole.
        :type: str
        """

        self._access_code = access_code

    @property
    def client_user_id(self):
        """
        Gets the client_user_id of this TemplateRole.
        Specifies whether the recipient is embedded or remote.   If the `clientUserId` property is not null then the recipient is embedded. Note that if the `ClientUserId` property is set and either `SignerMustHaveAccount` or `SignerMustLoginToSign` property of the account settings is set to  **true**, an error is generated on sending.ng.   Maximum length: 100 characters. 

        :return: The client_user_id of this TemplateRole.
        :rtype: str
        """
        return self._client_user_id

    @client_user_id.setter
    def client_user_id(self, client_user_id):
        """
        Sets the client_user_id of this TemplateRole.
        Specifies whether the recipient is embedded or remote.   If the `clientUserId` property is not null then the recipient is embedded. Note that if the `ClientUserId` property is set and either `SignerMustHaveAccount` or `SignerMustLoginToSign` property of the account settings is set to  **true**, an error is generated on sending.ng.   Maximum length: 100 characters. 

        :param client_user_id: The client_user_id of this TemplateRole.
        :type: str
        """

        self._client_user_id = client_user_id

    @property
    def default_recipient(self):
        """
        Gets the default_recipient of this TemplateRole.
        When set to **true**, this recipient is the default recipient and any tabs generated by the transformPdfFields option are mapped to this recipient.

        :return: The default_recipient of this TemplateRole.
        :rtype: str
        """
        return self._default_recipient

    @default_recipient.setter
    def default_recipient(self, default_recipient):
        """
        Sets the default_recipient of this TemplateRole.
        When set to **true**, this recipient is the default recipient and any tabs generated by the transformPdfFields option are mapped to this recipient.

        :param default_recipient: The default_recipient of this TemplateRole.
        :type: str
        """

        self._default_recipient = default_recipient

    @property
    def email(self):
        """
        Gets the email of this TemplateRole.
        Specifies the email associated with a role name.

        :return: The email of this TemplateRole.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this TemplateRole.
        Specifies the email associated with a role name.

        :param email: The email of this TemplateRole.
        :type: str
        """

        self._email = email

    @property
    def email_notification(self):
        """
        Gets the email_notification of this TemplateRole.

        :return: The email_notification of this TemplateRole.
        :rtype: RecipientEmailNotification
        """
        return self._email_notification

    @email_notification.setter
    def email_notification(self, email_notification):
        """
        Sets the email_notification of this TemplateRole.

        :param email_notification: The email_notification of this TemplateRole.
        :type: RecipientEmailNotification
        """

        self._email_notification = email_notification

    @property
    def embedded_recipient_start_url(self):
        """
        Gets the embedded_recipient_start_url of this TemplateRole.
        Specifies a sender provided valid URL string for redirecting an embedded recipient. When using this option, the embedded recipient still receives an email from DocuSign, just as a remote recipient would. When the document link in the email is clicked the recipient is redirected, through DocuSign, to the supplied URL to complete their actions. When routing to the URL, the sender’s system (the server responding to the URL) must request a recipient token to launch a signing session.   If set to `SIGN_AT_DOCUSIGN`, the recipient is directed to an embedded signing or viewing process directly at DocuSign. The signing or viewing action is initiated by the DocuSign system and the transaction activity and Certificate of Completion records will reflect this. In all other ways the process is identical to an embedded signing or viewing operation that is launched by any partner.  It is important to remember that in a typical embedded workflow the authentication of an embedded recipient is the responsibility of the sending application, DocuSign expects that senders will follow their own process for establishing the recipient’s identity. In this workflow the recipient goes through the sending application before the embedded signing or viewing process in initiated. However, when the sending application sets `EmbeddedRecipientStartURL=SIGN_AT_DOCUSIGN`, the recipient goes directly to the embedded signing or viewing process bypassing the sending application and any authentication steps the sending application would use. In this case, DocuSign recommends that you use one of the normal DocuSign authentication features (Access Code, Phone Authentication, SMS Authentication, etc.) to verify the identity of the recipient.  If the `clientUserId` property is NOT set, and the `embeddedRecipientStartURL` is set, DocuSign will ignore the redirect URL and launch the standard signing process for the email recipient. Information can be appended to the embedded recipient start URL using merge fields. The available merge fields items are: envelopeId, recipientId, recipientName, recipientEmail, and customFields. The `customFields` property must be set fort the recipient or envelope. The merge fields are enclosed in double brackets.   *Example*:   `http://senderHost/[[mergeField1]]/ beginSigningSession? [[mergeField2]]&[[mergeField3]]` 

        :return: The embedded_recipient_start_url of this TemplateRole.
        :rtype: str
        """
        return self._embedded_recipient_start_url

    @embedded_recipient_start_url.setter
    def embedded_recipient_start_url(self, embedded_recipient_start_url):
        """
        Sets the embedded_recipient_start_url of this TemplateRole.
        Specifies a sender provided valid URL string for redirecting an embedded recipient. When using this option, the embedded recipient still receives an email from DocuSign, just as a remote recipient would. When the document link in the email is clicked the recipient is redirected, through DocuSign, to the supplied URL to complete their actions. When routing to the URL, the sender’s system (the server responding to the URL) must request a recipient token to launch a signing session.   If set to `SIGN_AT_DOCUSIGN`, the recipient is directed to an embedded signing or viewing process directly at DocuSign. The signing or viewing action is initiated by the DocuSign system and the transaction activity and Certificate of Completion records will reflect this. In all other ways the process is identical to an embedded signing or viewing operation that is launched by any partner.  It is important to remember that in a typical embedded workflow the authentication of an embedded recipient is the responsibility of the sending application, DocuSign expects that senders will follow their own process for establishing the recipient’s identity. In this workflow the recipient goes through the sending application before the embedded signing or viewing process in initiated. However, when the sending application sets `EmbeddedRecipientStartURL=SIGN_AT_DOCUSIGN`, the recipient goes directly to the embedded signing or viewing process bypassing the sending application and any authentication steps the sending application would use. In this case, DocuSign recommends that you use one of the normal DocuSign authentication features (Access Code, Phone Authentication, SMS Authentication, etc.) to verify the identity of the recipient.  If the `clientUserId` property is NOT set, and the `embeddedRecipientStartURL` is set, DocuSign will ignore the redirect URL and launch the standard signing process for the email recipient. Information can be appended to the embedded recipient start URL using merge fields. The available merge fields items are: envelopeId, recipientId, recipientName, recipientEmail, and customFields. The `customFields` property must be set fort the recipient or envelope. The merge fields are enclosed in double brackets.   *Example*:   `http://senderHost/[[mergeField1]]/ beginSigningSession? [[mergeField2]]&[[mergeField3]]` 

        :param embedded_recipient_start_url: The embedded_recipient_start_url of this TemplateRole.
        :type: str
        """

        self._embedded_recipient_start_url = embedded_recipient_start_url

    @property
    def in_person_signer_name(self):
        """
        Gets the in_person_signer_name of this TemplateRole.
        Specifies the full legal name of the signer in person signer template roles.  Maximum Length: 100 characters.

        :return: The in_person_signer_name of this TemplateRole.
        :rtype: str
        """
        return self._in_person_signer_name

    @in_person_signer_name.setter
    def in_person_signer_name(self, in_person_signer_name):
        """
        Sets the in_person_signer_name of this TemplateRole.
        Specifies the full legal name of the signer in person signer template roles.  Maximum Length: 100 characters.

        :param in_person_signer_name: The in_person_signer_name of this TemplateRole.
        :type: str
        """

        self._in_person_signer_name = in_person_signer_name

    @property
    def name(self):
        """
        Gets the name of this TemplateRole.
        Specifies the recipient's name.

        :return: The name of this TemplateRole.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this TemplateRole.
        Specifies the recipient's name.

        :param name: The name of this TemplateRole.
        :type: str
        """

        self._name = name

    @property
    def recipient_signature_providers(self):
        """
        Gets the recipient_signature_providers of this TemplateRole.
        

        :return: The recipient_signature_providers of this TemplateRole.
        :rtype: list[RecipientSignatureProvider]
        """
        return self._recipient_signature_providers

    @recipient_signature_providers.setter
    def recipient_signature_providers(self, recipient_signature_providers):
        """
        Sets the recipient_signature_providers of this TemplateRole.
        

        :param recipient_signature_providers: The recipient_signature_providers of this TemplateRole.
        :type: list[RecipientSignatureProvider]
        """

        self._recipient_signature_providers = recipient_signature_providers

    @property
    def role_name(self):
        """
        Gets the role_name of this TemplateRole.
        Optional element. Specifies the role name associated with the recipient.<br/><br/>This is required when working with template recipients.

        :return: The role_name of this TemplateRole.
        :rtype: str
        """
        return self._role_name

    @role_name.setter
    def role_name(self, role_name):
        """
        Sets the role_name of this TemplateRole.
        Optional element. Specifies the role name associated with the recipient.<br/><br/>This is required when working with template recipients.

        :param role_name: The role_name of this TemplateRole.
        :type: str
        """

        self._role_name = role_name

    @property
    def routing_order(self):
        """
        Gets the routing_order of this TemplateRole.
        Specifies the routing order of the recipient in the envelope. 

        :return: The routing_order of this TemplateRole.
        :rtype: str
        """
        return self._routing_order

    @routing_order.setter
    def routing_order(self, routing_order):
        """
        Sets the routing_order of this TemplateRole.
        Specifies the routing order of the recipient in the envelope. 

        :param routing_order: The routing_order of this TemplateRole.
        :type: str
        """

        self._routing_order = routing_order

    @property
    def signing_group_id(self):
        """
        Gets the signing_group_id of this TemplateRole.
        When set to **true** and the feature is enabled in the sender's account, the signing recipient is required to draw signatures and initials at each signature/initial tab ( instead of adopting a signature/initial style or only drawing a signature/initial once).

        :return: The signing_group_id of this TemplateRole.
        :rtype: str
        """
        return self._signing_group_id

    @signing_group_id.setter
    def signing_group_id(self, signing_group_id):
        """
        Sets the signing_group_id of this TemplateRole.
        When set to **true** and the feature is enabled in the sender's account, the signing recipient is required to draw signatures and initials at each signature/initial tab ( instead of adopting a signature/initial style or only drawing a signature/initial once).

        :param signing_group_id: The signing_group_id of this TemplateRole.
        :type: str
        """

        self._signing_group_id = signing_group_id

    @property
    def tabs(self):
        """
        Gets the tabs of this TemplateRole.

        :return: The tabs of this TemplateRole.
        :rtype: Tabs
        """
        return self._tabs

    @tabs.setter
    def tabs(self, tabs):
        """
        Sets the tabs of this TemplateRole.

        :param tabs: The tabs of this TemplateRole.
        :type: Tabs
        """

        self._tabs = tabs

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
