"""Manager utility implementations of assessment.authoring managers."""
# pylint: disable=no-init
#     Numerous classes don't require __init__.
# pylint: disable=too-many-public-methods
#     Number of methods are defined in specification
# pylint: disable=too-many-ancestors
#     Inheritance defined in specification


from ..osid import managers as osid_managers
from ..osid.osid_errors import NullArgument
from ..osid.osid_errors import Unimplemented
from ..type.objects import TypeList
from dlkit.abstract_osid.assessment_authoring import managers as abc_assessment_authoring_managers


class AssessmentAuthoringProfile(abc_assessment_authoring_managers.AssessmentAuthoringProfile, osid_managers.OsidProfile):
    """The ``AssessmentAuthoringProfile`` describes the interoperability among assessment authoring services."""

    def supports_visible_federation(self):
        """Tests if federation is visible.

        return: (boolean) - ``true`` if visible federation is supported
                ``,``  ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_lookup(self):
        """Tests if looking up assessment part is supported.

        return: (boolean) - ``true`` if assessment part lookup is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_query(self):
        """Tests if querying assessment part is supported.

        return: (boolean) - ``true`` if assessment part query is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_search(self):
        """Tests if searching assessment part is supported.

        return: (boolean) - ``true`` if assessment part search is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_admin(self):
        """Tests if an assessment part administrative service is supported.

        return: (boolean) - ``true`` if assessment part administration
                is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_notification(self):
        """Tests if an assessment part notification service is supported.

        return: (boolean) - ``true`` if assessment part notification is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_bank(self):
        """Tests if an assessment part bank lookup service is supported.

        return: (boolean) - ``true`` if an assessment part bank lookup
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_bank_assignment(self):
        """Tests if an assessment part bank service is supported.

        return: (boolean) - ``true`` if assessment part bank assignment
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_smart_bank(self):
        """Tests if an assessment part bank lookup service is supported.

        return: (boolean) - ``true`` if an assessment part bank service
                is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_item(self):
        """Tests if an assessment part item service is supported for looking up assessment part and item mappings.

        return: (boolean) - ``true`` if assessment part item service is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_assessment_part_item_design(self):
        """Tests if an assessment part item design session is supported.

        return: (boolean) - ``true`` if an assessment part item design
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_lookup(self):
        """Tests if looking up sequence rule is supported.

        return: (boolean) - ``true`` if sequence rule lookup is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_query(self):
        """Tests if querying sequence rule is supported.

        return: (boolean) - ``true`` if sequence rule query is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_search(self):
        """Tests if searching sequence rule is supported.

        return: (boolean) - ``true`` if sequence rule search is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_admin(self):
        """Tests if a sequence rule administrative service is supported.

        return: (boolean) - ``true`` if sequence rule administration is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_notification(self):
        """Tests if a sequence rule notification service is supported.

        return: (boolean) - ``true`` if sequence rule notification is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_bank(self):
        """Tests if a sequence rule bank lookup service is supported.

        return: (boolean) - ``true`` if a sequence rule bank lookup
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_bank_assignment(self):
        """Tests if a sequence rule bank service is supported.

        return: (boolean) - ``true`` if sequence rule bank assignment
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_smart_bank(self):
        """Tests if a sequence rule bank lookup service is supported.

        return: (boolean) - ``true`` if a sequence rule bank service is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_lookup(self):
        """Tests if looking up sequence rule enablers is supported.

        return: (boolean) - ``true`` if sequence rule enabler lookup is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_query(self):
        """Tests if querying sequence rule enablers is supported.

        return: (boolean) - ``true`` if sequence rule enabler query is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_search(self):
        """Tests if searching sequence rule enablers is supported.

        return: (boolean) - ``true`` if sequence rule enabler search is
                supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_admin(self):
        """Tests if a sequence rule enabler administrative service is supported.

        return: (boolean) - ``true`` if sequence rule enabler
                administration is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_notification(self):
        """Tests if a sequence rule enabler notification service is supported.

        return: (boolean) - ``true`` if sequence rule enabler
                notification is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_bank(self):
        """Tests if a sequence rule enabler bank lookup service is supported.

        return: (boolean) - ``true`` if a sequence rule enabler bank
                lookup service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_bank_assignment(self):
        """Tests if a sequence rule enabler bank service is supported.

        return: (boolean) - ``true`` if sequence rule enabler bank
                assignment service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_smart_bank(self):
        """Tests if a sequence rule enabler bank lookup service is supported.

        return: (boolean) - ``true`` if a sequence rule enabler bank
                service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_rule_lookup(self):
        """Tests if a sequence rule enabler rule lookup service is supported.

        return: (boolean) - ``true`` if a sequence rule enabler rule
                lookup service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def supports_sequence_rule_enabler_rule_application(self):
        """Tests if a sequence rule enabler rule application service is supported.

        return: (boolean) - ``true`` if sequence rule enabler rule
                application service is supported, ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def get_assessment_part_record_types(self):
        """Gets the supported ``AssessmentPart`` record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``AssessmentPart`` record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    assessment_part_record_types = property(fget=get_assessment_part_record_types)

    def supports_assessment_part_record_type(self, assessment_part_record_type=None):
        """Tests if the given ``AssessmentPart`` record type is supported.

        arg:    assessment_part_record_type (osid.type.Type): a ``Type``
                indicating an ``AssessmentPart`` record type
        return: (boolean) - ``true`` if the given record type is
                supported, ``false`` otherwise
        raise:  NullArgument - ``assessment_part_record_type`` is
                ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if assessment_part_record_type is None:
            raise NullArgument()
        return False

    def get_assessment_part_search_record_types(self):
        """Gets the supported ``AssessmentPart`` search record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``AssessmentPart`` search record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    assessment_part_search_record_types = property(fget=get_assessment_part_search_record_types)

    def supports_assessment_part_search_record_type(self, assessment_part_search_record_type=None):
        """Tests if the given ``AssessmentPart`` search record type is supported.

        arg:    assessment_part_search_record_type (osid.type.Type): a
                ``Type`` indicating an ``AssessmentPart`` search record
                type
        return: (boolean) - ``true`` if the given search record type is
                supported, ``false`` otherwise
        raise:  NullArgument - ``assessment_part_search_record_type`` is
                ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if assessment_part_search_record_type is None:
            raise NullArgument()
        return False

    def get_sequence_rule_record_types(self):
        """Gets the supported ``SequenceRule`` record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``SequenceRule`` record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    sequence_rule_record_types = property(fget=get_sequence_rule_record_types)

    def supports_sequence_rule_record_type(self, sequence_rule_record_type=None):
        """Tests if the given ``SequenceRule`` record type is supported.

        arg:    sequence_rule_record_type (osid.type.Type): a ``Type``
                indicating a ``SequenceRule`` record type
        return: (boolean) - ``true`` if the given record type is
                supported, ``false`` otherwise
        raise:  NullArgument - ``sequence_rule_record_type`` is ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if sequence_rule_record_type is None:
            raise NullArgument()
        return False

    def get_sequence_rule_search_record_types(self):
        """Gets the supported ``SequenceRule`` search record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``SequenceRule`` search record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    sequence_rule_search_record_types = property(fget=get_sequence_rule_search_record_types)

    def supports_sequence_rule_search_record_type(self, sequence_rule_search_record_type=None):
        """Tests if the given ``SequenceRule`` search record type is supported.

        arg:    sequence_rule_search_record_type (osid.type.Type): a
                ``Type`` indicating a ``SequenceRule`` search record
                type
        return: (boolean) - ``true`` if the given search record type is
                supported, ``false`` otherwise
        raise:  NullArgument - ``sequence_rule_search_record_type`` is
                ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if sequence_rule_search_record_type is None:
            raise NullArgument()
        return False

    def get_sequence_rule_enabler_record_types(self):
        """Gets the supported ``SequenceRuleEnabler`` record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``SequenceRuleEnabler`` record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    sequence_rule_enabler_record_types = property(fget=get_sequence_rule_enabler_record_types)

    def supports_sequence_rule_enabler_record_type(self, sequence_rule_enabler_record_type=None):
        """Tests if the given ``SequenceRuleEnabler`` record type is supported.

        arg:    sequence_rule_enabler_record_type (osid.type.Type): a
                ``Type`` indicating a ``SequenceRuleEnabler`` record
                type
        return: (boolean) - ``true`` if the given record type is
                supported, ``false`` otherwise
        raise:  NullArgument - ``sequence_rule_enabler_record_type`` is
                ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if sequence_rule_enabler_record_type is None:
            raise NullArgument()
        return False

    def get_sequence_rule_enabler_search_record_types(self):
        """Gets the supported ``SequenceRuleEnabler`` search record types.

        return: (osid.type.TypeList) - a list containing the supported
                ``SequenceRuleEnabler`` search record types
        *compliance: mandatory -- This method must be implemented.*

        """
        return TypeList([])

    sequence_rule_enabler_search_record_types = property(fget=get_sequence_rule_enabler_search_record_types)

    def supports_sequence_rule_enabler_search_record_type(self, sequence_rule_enabler_search_record_type=None):
        """Tests if the given ``SequenceRuleEnabler`` search record type is supported.

        arg:    sequence_rule_enabler_search_record_type
                (osid.type.Type): a ``Type`` indicating a
                ``SequenceRuleEnabler`` search record type
        return: (boolean) - ``true`` if the given search record type is
                supported, ``false`` otherwise
        raise:  NullArgument -
                ``sequence_rule_enabler_search_record_type`` is ``null``
        *compliance: mandatory -- This method must be implemented.*

        """
        if sequence_rule_enabler_search_record_type is None:
            raise NullArgument()
        return False


class AssessmentAuthoringManager(abc_assessment_authoring_managers.AssessmentAuthoringManager, osid_managers.OsidManager, AssessmentAuthoringProfile):
    """The assessment authoring manager provides access to assessment authoring sessions and provides interoperability tests for various aspects of this service.

    The sessions included in this manager are:

      * ``AssessmentPartLookupSession:`` a session to retrieve
        assessment part
      * ``AssessmentPartQuerySession:`` a session to query for
        assessment part
      * ``AssessmentPartSearchSession:`` a session to search for
        assessment part
      * ``AssessmentPartAdminSession:`` a session to create and delete
        assessment part
      * ``AssessmentPartNotificationSession:`` a session to receive
        notifications pertaining to assessment part changes
      * ``AssessmentPartBankSession:`` a session to look up assessment
        part bank mappings
      * ``AssessmentPartBankAssignmentSession:`` a session to manage
        assessment part to bank mappings
      * ``AssessmentPartSmartBankSession:`` a session to manage dynamic
        bank of assessment part
      * ``AssessmentPartItemSession:`` a session to look up assessment
        part to item mappings
      * ``AssessmentPartItemDesignSession:`` a session to map items to
        assessment parts

      * ``SequenceRuleLookupSession:`` a session to retrieve sequence
        rule
      * ``SequenceRuleQuerySession:`` a session to query for sequence
        rule
      * ``SequenceRuleSearchSession:`` a session to search for sequence
        rule
      * ``SequenceRuleAdminSession:`` a session to create and delete
        sequence rule
      * ``SequenceRuleNotificationSession:`` a session to receive
        notifications pertaining to sequence rule changes
      * ``SequenceRuleBankSession:`` a session to look up sequence rule
        bank mappings
      * ``SequenceRuleBankAssignmentSession:`` a session to manage
        sequence rule to bank mappings
      * ``SequenceRuleSmartBankSession:`` a session to manage dynamic
        bank of sequence rule

      * ``SequenceRuleEnablerLookupSession:`` a session to retrieve
        sequence rule enablers
      * ``SequenceRuleEnablerQuerySession:`` a session to query for
        sequence rule enablers
      * ``SequenceRuleEnablerSearchSession:`` a session to search for
        sequence rule enablers
      * ``SequenceRuleEnablerAdminSession:`` a session to create and
        delete sequence rule enablers
      * ``SequenceRuleEnablerNotificationSession:`` a session to receive
        notifications pertaining to sequence rule enabler changes
      * ``SequenceRuleEnablerBankSession:`` a session to look up
        sequence rule enabler bank mappings
      * ``SequenceRuleEnablerBankAssignmentSession:`` a session to
        manage sequence rule enabler to bank mappings
      * ``SequenceRuleEnablerSmartBankSession:`` a session to manage
        dynamic bank of sequence rule enablers
      * ``SequenceRuleEnableRuleLookupSession:`` a session to look up
        sequence rule enabler mappings
      * ``SequenceRuleEnablerRuleApplicationSession:`` a session to
        apply sequence rule enablers

    """

    def get_assessment_part_lookup_session(self):
        """Gets the ``OsidSession`` associated with the assessment part lookup service.

        return: (osid.assessment.authoring.AssessmentPartLookupSession)
                - an ``AssessmentPartLookupSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_lookup()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_lookup_session = property(fget=get_assessment_part_lookup_session)

    def get_assessment_part_lookup_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the assessment part lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.AssessmentPartLookupSession)
                - an ``AssessmentPartLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_query_session(self):
        """Gets the ``OsidSession`` associated with the assessment part query service.

        return: (osid.assessment.authoring.AssessmentPartQuerySession) -
                an ``AssessmentPartQuerySession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_query()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_query()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_query_session = property(fget=get_assessment_part_query_session)

    def get_assessment_part_query_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the assessment part query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.AssessmentPartQuerySession) -
                an ``AssessmentPartQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_search_session(self):
        """Gets the ``OsidSession`` associated with the assessment part search service.

        return: (osid.assessment.authoring.AssessmentPartSearchSession)
                - an ``AssessmentPartSearchSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_search()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_search()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_search_session = property(fget=get_assessment_part_search_session)

    def get_assessment_part_search_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the assessment part earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.AssessmentPartSearchSession)
                - an ``AssessmentPartSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_admin_session(self):
        """Gets the ``OsidSession`` associated with the assessment part administration service.

        return: (osid.assessment.authoring.AssessmentPartAdminSession) -
                an ``AssessmentPartAdminSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_admin()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_admin()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_admin_session = property(fget=get_assessment_part_admin_session)

    def get_assessment_part_admin_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the assessment part administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.AssessmentPartAdminSession) -
                an ``AssessmentPartAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_notification_session(self, assessment_part_receiver=None):
        """Gets the ``OsidSession`` associated with the assessment part notification service.

        arg:    assessment_part_receiver
                (osid.assessment.authoring.AssessmentPartReceiver): the
                notification callback
        return:
                (osid.assessment.authoring.AssessmentPartNotificationSes
                sion) - an ``AssessmentPartNotificationSession``
        raise:  NullArgument - ``assessment_part_receiver`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_notification()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_notification()`` is ``true``.*

        """
        raise Unimplemented()

    def get_assessment_part_notification_session_for_bank(self, assessment_part_receiver=None, bank_id=None):
        """Gets the ``OsidSession`` associated with the assessment part notification service for the given bank.

        arg:    assessment_part_receiver
                (osid.assessment.authoring.AssessmentPartReceiver): the
                notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.AssessmentPartNotificationSes
                sion) - an ``AssessmentPartNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``assessment_part_receiver`` or
                ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if assessment_part_receiver is None:
            raise NullArgument
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_bank_session(self):
        """Gets the ``OsidSession`` to lookup assessment part/bank mappings for assessment parts.

        return: (osid.assessment.authoring.AssessmentPartBankSession) -
                an ``AssessmentPartBankSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_bank()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_bank_session = property(fget=get_assessment_part_bank_session)

    def get_assessment_part_bank_assignment_session(self):
        """Gets the ``OsidSession`` associated with assigning assessment part to bank.

        return:
                (osid.assessment.authoring.AssessmentPartBankAssignmentS
                ession) - an ``AssessmentPartBankAssignmentSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_bank_assignment()`` is ``true``.*

        """
        raise Unimplemented()

    assessment_part_bank_assignment_session = property(fget=get_assessment_part_bank_assignment_session)

    def get_assessment_part_smart_bank_session(self, bank_id=None):
        """Gets the ``OsidSession`` to manage assessment part smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.AssessmentPartSmartBankSessio
                n) - an ``AssessmentPartSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_smart_bank()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_smart_bank()`` is ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_lookup_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule lookup service.

        return: (osid.assessment.authoring.SequenceRuleLookupSession) -
                a ``SequenceRuleLookupSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_lookup()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_lookup_session = property(fget=get_sequence_rule_lookup_session)

    def get_sequence_rule_lookup_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleLookupSession) -
                a ``SequenceRuleLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_query_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule query service.

        return: (osid.assessment.authoring.SequenceRuleQuerySession) - a
                ``SequenceRuleQuerySession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_query()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_query()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_query_session = property(fget=get_sequence_rule_query_session)

    def get_sequence_rule_query_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleQuerySession) - a
                ``SequenceRuleQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_search_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule search service.

        return: (osid.assessment.authoring.SequenceRuleSearchSession) -
                a ``SequenceRuleSearchSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_search()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_search()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_search_session = property(fget=get_sequence_rule_search_session)

    def get_sequence_rule_search_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleSearchSession) -
                a ``SequenceRuleSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_admin_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule administration service.

        return: (osid.assessment.authoring.SequenceRuleAdminSession) - a
                ``SequenceRuleAdminSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_admin()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_admin()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_admin_session = property(fget=get_sequence_rule_admin_session)

    def get_sequence_rule_admin_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleAdminSession) - a
                ``SequenceRuleAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_notification_session(self, sequence_rule_receiver=None):
        """Gets the ``OsidSession`` associated with the sequence rule notification service.

        arg:    sequence_rule_receiver
                (osid.assessment.authoring.SequenceRuleReceiver): the
                notification callback
        return:
                (osid.assessment.authoring.SequenceRuleNotificationSessi
                on) - a ``SequenceRuleNotificationSession``
        raise:  NullArgument - ``sequence_rule_receiver`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_notification()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_notification()`` is ``true``.*

        """
        raise Unimplemented()

    def get_sequence_rule_notification_session_for_bank(self, sequence_rule_receiver=None, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule notification service for the given bank.

        arg:    sequence_rule_receiver
                (osid.assessment.authoring.SequenceRuleReceiver): the
                notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleNotificationSessi
                on) - a ``SequenceRuleNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``sequence_rule_receiver`` or ``bank_id``
                is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if sequence_rule_receiver is None:
            raise NullArgument
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_bank_session(self):
        """Gets the ``OsidSession`` to lookup sequence rule/bank mappings for sequence rules.

        return: (osid.assessment.authoring.SequenceRuleBankSession) - a
                ``SequenceRuleBankSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_bank()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_bank_session = property(fget=get_sequence_rule_bank_session)

    def get_sequence_rule_bank_assignment_session(self):
        """Gets the ``OsidSession`` associated with assigning sequence rule to bank.

        return:
                (osid.assessment.authoring.SequenceRuleBankAssignmentSes
                sion) - a ``SequenceRuleBankAssignmentSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_bank_assignment()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_bank_assignment_session = property(fget=get_sequence_rule_bank_assignment_session)

    def get_sequence_rule_smart_bank_session(self, bank_id=None):
        """Gets the ``OsidSession`` to manage sequence rule smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleSmartBankSession)
                - a ``SequenceRuleSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_smart_bank()``
                is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_smart_bank()`` is ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_lookup_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler lookup service.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerLookupSess
                ion) - a ``SequenceRuleEnablerLookupSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_lookup()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_lookup()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_lookup_session = property(fget=get_sequence_rule_enabler_lookup_session)

    def get_sequence_rule_enabler_lookup_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerLookupSess
                ion) - a ``SequenceRuleEnablerLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_query_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler query service.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerQuerySessi
                on) - a ``SequenceRuleEnablerQuerySession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_query()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_query()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_query_session = property(fget=get_sequence_rule_enabler_query_session)

    def get_sequence_rule_enabler_query_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerQuerySessi
                on) - a ``SequenceRuleEnablerQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_search_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler search service.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerSearchSess
                ion) - a ``SequenceRuleEnablerSearchSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_search()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_search()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_search_session = property(fget=get_sequence_rule_enabler_search_session)

    def get_sequence_rule_enabler_search_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enablers earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerSearchSess
                ion) - a ``SequenceRuleEnablerSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_admin_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler administration service.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerAdminSessi
                on) - a ``SequenceRuleEnablerAdminSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_admin()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_admin()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_admin_session = property(fget=get_sequence_rule_enabler_admin_session)

    def get_sequence_rule_enabler_admin_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerAdminSessi
                on) - a ``SequenceRuleEnablerAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_notification_session(self, sequence_rule_enabler_receiver=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler notification service.

        arg:    sequence_rule_enabler_receiver
                (osid.assessment.authoring.SequenceRuleEnablerReceiver):
                the notification callback
        return: (osid.assessment.authoring.SequenceRuleEnablerNotificati
                onSession) - a
                ``SequenceRuleEnablerNotificationSession``
        raise:  NullArgument - ``sequence_rule_enabler_receiver`` is
                ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_notification()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_notification()`` is ``true``.*

        """
        raise Unimplemented()

    def get_sequence_rule_enabler_notification_session_for_bank(self, sequence_rule_enabler_receiver=None, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler notification service for the given bank.

        arg:    sequence_rule_enabler_receiver
                (osid.assessment.authoring.SequenceRuleEnablerReceiver):
                the notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleEnablerNotificati
                onSession) - a
                ``SequenceRuleEnablerNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``sequence_rule_enabler_receiver`` or
                ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if sequence_rule_enabler_receiver is None:
            raise NullArgument
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_bank_session(self):
        """Gets the ``OsidSession`` to lookup sequence rule enabler/bank mappings for sequence rule enablers.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerBankSessio
                n) - a ``SequenceRuleEnablerBankSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_bank()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_bank()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_bank_session = property(fget=get_sequence_rule_enabler_bank_session)

    def get_sequence_rule_enabler_bank_assignment_session(self):
        """Gets the ``OsidSession`` associated with assigning sequence rule enablers to bank.

        return: (osid.assessment.authoring.SequenceRuleEnablerBankAssign
                mentSession) - a
                ``SequenceRuleEnablerBankAssignmentSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_bank_assignment()`` is
        ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_bank_assignment_session = property(fget=get_sequence_rule_enabler_bank_assignment_session)

    def get_sequence_rule_enabler_smart_bank_session(self, bank_id=None):
        """Gets the ``OsidSession`` to manage sequence rule enabler smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerSmartBankS
                ession) - a ``SequenceRuleEnablerSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_smart_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_smart_bank()`` is ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_lookup_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler mapping lookup service.

        return:
                (osid.assessment.authoring.SequenceRuleEnablerRuleLookup
                Session) - a ``SequenceRuleEnablerRuleLookupSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_lookup()`` is ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_rule_lookup_session = property(fget=get_sequence_rule_enabler_rule_lookup_session)

    def get_sequence_rule_enabler_rule_lookup_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler mapping lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return:
                (osid.assessment.authoring.SequenceRuleEnablerRuleLookup
                Session) - a ``SequenceRuleEnablerRuleLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_application_session(self):
        """Gets the ``OsidSession`` associated with the sequence rule enabler assignment service.

        return: (osid.assessment.authoring.SequenceRuleEnablerRuleApplic
                ationSession) - a
                ``SequenceRuleEnablerRuleApplicationSession``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_application()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_application()`` is
        ``true``.*

        """
        raise Unimplemented()

    sequence_rule_enabler_rule_application_session = property(fget=get_sequence_rule_enabler_rule_application_session)

    def get_sequence_rule_enabler_rule_application_session_for_bank(self, bank_id=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler assignment service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        return: (osid.assessment.authoring.SequenceRuleEnablerRuleApplic
                ationSession) - a
                ``SequenceRuleEnablerRuleApplicationSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_application()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_application()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None:
            raise NullArgument
        raise Unimplemented()


class AssessmentAuthoringProxyManager(abc_assessment_authoring_managers.AssessmentAuthoringProxyManager, osid_managers.OsidProxyManager, AssessmentAuthoringProfile):
    """The assessment authoring manager provides access to assessment authoring sessions and provides interoperability tests for various aspects of this service.

    Methods in this manager support the passing of a ``Proxy`` object.
    The sessions included in this manager are:

      * ``AssessmentPartLookupSession:`` a session to retrieve
        assessment part
      * ``AssessmentPartQuerySession:`` a session to query for
        assessment part
      * ``AssessmentPartSearchSession:`` a session to search for
        assessment part
      * ``AssessmentPartAdminSession:`` a session to create and delete
        assessment part
      * ``AssessmentPartNotificationSession:`` a session to receive
        notifications pertaining to assessment part changes
      * ``AssessmentPartBankSession:`` a session to look up assessment
        part bank mappings
      * ``AssessmentPartBankAssignmentSession:`` a session to manage
        assessment part to bank mappings
      * ``AssessmentPartSmartBankSession:`` a session to manage dynamic
        bank of assessment part
      * ``AssessmentPartItemSession:`` a session to look up assessment
        part to item mappings
      * ``AssessmentPartItemDesignSession:`` a session to map items to
        assessment parts

      * ``SequenceRuleLookupSession:`` a session to retrieve sequence
        rule
      * ``SequenceRuleQuerySession:`` a session to query for sequence
        rule
      * ``SequenceRuleSearchSession:`` a session to search for sequence
        rule
      * ``SequenceRuleAdminSession:`` a session to create and delete
        sequence rule
      * ``SequenceRuleNotificationSession:`` a session to receive
        notifications pertaining to sequence rule changes
      * ``SequenceRuleBankSession:`` a session to look up sequence rule
        bank mappings
      * ``SequenceRuleBankAssignmentSession:`` a session to manage
        sequence rule to bank mappings
      * ``SequenceRuleSmartBankSession:`` a session to manage dynamic
        bank of sequence rule

      * ``SequenceRuleEnablerLookupSession:`` a session to retrieve
        sequence rule enablers
      * ``SequenceRuleEnablerQuerySession:`` a session to query for
        sequence rule enablers
      * ``SequenceRuleEnablerSearchSession:`` a session to search for
        sequence rule enablers
      * ``SequenceRuleEnablerAdminSession:`` a session to create and
        delete sequence rule enablers
      * ``SequenceRuleEnablerNotificationSession:`` a session to receive
        notifications pertaining to sequence rule enabler changes
      * ``SequenceRuleEnablerBankSession:`` a session to look up
        sequence rule enabler bank mappings
      * ``SequenceRuleEnablerBankAssignmentSession:`` a session to
        manage sequence rule enabler to bank mappings
      * ``SequenceRuleEnablerSmartBankSession:`` a session to manage
        dynamic bank of sequence rule enablers
      * ``SequenceRuleEnableRuleLookupSession:`` a session to look up
        sequence rule enabler mappings
      * ``SequenceRuleEnablerRuleApplicationSession:`` a session to
        apply sequence rule enablers

    """

    def get_assessment_part_lookup_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part lookup service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartLookupSession)
                - an ``AssessmentPartLookupSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_lookup()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_lookup_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartLookupSession)
                - an ``AssessmentPartLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_query_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part query service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartQuerySession) -
                an ``AssessmentPartQuerySession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_query()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_query()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_query_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartQuerySession) -
                an ``AssessmentPartQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_search_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part search service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartSearchSession)
                - an ``AssessmentPartSearchSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_search()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_search()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_search_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartSearchSession)
                - an ``AssessmentPartSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_admin_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part administration service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartAdminSession) -
                an ``AssessmentPartAdminSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_admin()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_admin()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_admin_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartAdminSession) -
                an ``AssessmentPartAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_notification_session(self, assessment_part_receiver=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part notification service.

        arg:    assessment_part_receiver
                (osid.assessment.authoring.AssessmentPartReceiver): the
                notification callback
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.AssessmentPartNotificationSes
                sion) - an ``AssessmentPartNotificationSession``
        raise:  NullArgument - ``assessment_part_receiver`` or ``proxy``
                is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_notification()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_notification()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_notification_session_for_bank(self, assessment_part_receiver=None, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the assessment part notification service for the given bank.

        arg:    assessment_part_receiver
                (osid.assessment.authoring.AssessmentPartReceiver): the
                notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.AssessmentPartNotificationSes
                sion) - an ``AssessmentPartNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``assessment_part_receiver, bank_id`` or
                ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if assessment_part_receiver is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_assessment_part_bank_session(self, proxy=None):
        """Gets the ``OsidSession`` to lookup assessment part/bank mappings for assessment parts.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.AssessmentPartBankSession) -
                an ``AssessmentPartBankSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_assessment_part_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_bank_assignment_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with assigning assessment part to bank.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.AssessmentPartBankAssignmentS
                ession) - an ``AssessmentPartBankAssignmentSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_bank_assignment()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_assessment_part_smart_bank_session(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` to manage assessment part smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.AssessmentPartSmartBankSessio
                n) - an ``AssessmentPartSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_assessment_part_smart_bank()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_assessment_part_smart_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_lookup_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule lookup service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleLookupSession) -
                a ``SequenceRuleLookupSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_lookup()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_lookup_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleLookupSession) -
                a ``SequenceRuleLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_query_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule query service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleQuerySession) - a
                ``SequenceRuleQuerySession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_query()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_query()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_query_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleQuerySession) - a
                ``SequenceRuleQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_search_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule search service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleSearchSession) -
                a ``SequenceRuleSearchSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_search()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_search()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_search_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleSearchSession) -
                a ``SequenceRuleSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_admin_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule administration service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleAdminSession) - a
                ``SequenceRuleAdminSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_admin()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_admin()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_admin_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleAdminSession) - a
                ``SequenceRuleAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_notification_session(self, sequence_rule_receiver=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule notification service.

        arg:    sequence_rule_receiver
                (osid.assessment.authoring.SequenceRuleReceiver): the
                notification callback
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleNotificationSessi
                on) - a ``SequenceRuleNotificationSession``
        raise:  NullArgument - ``sequence_rule_receiver`` or ``proxy``
                is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_notification()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_notification()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_notification_session_for_bank(self, sequence_rule_receiver=None, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule notification service for the given bank.

        arg:    sequence_rule_receiver
                (osid.assessment.authoring.SequenceRuleReceiver): the
                notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleNotificationSessi
                on) - a ``SequenceRuleNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``sequence_rule_receiver, bank_id`` or
                ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if sequence_rule_receiver is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_bank_session(self, proxy=None):
        """Gets the ``OsidSession`` to lookup sequence rule/bank mappings for sequence rules.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleBankSession) - a
                ``SequenceRuleBankSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_bank_assignment_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with assigning sequence rule to bank.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleBankAssignmentSes
                sion) - a ``SequenceRuleBankAssignmentSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_bank_assignment()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_smart_bank_session(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` to manage sequence rule smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleSmartBankSession)
                - a ``SequenceRuleSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented - ``supports_sequence_rule_smart_bank()``
                is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_smart_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_lookup_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler lookup service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerLookupSess
                ion) - a ``SequenceRuleEnablerLookupSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_lookup()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_lookup()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_lookup_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerLookupSess
                ion) - a ``SequenceRuleEnablerLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_query_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler query service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerQuerySessi
                on) - a ``SequenceRuleEnablerQuerySession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_query()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_query()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_query_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler query service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerQuerySessi
                on) - a ``SequenceRuleEnablerQuerySession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_query()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_query()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_search_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler search service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerSearchSess
                ion) - a ``SequenceRuleEnablerSearchSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_search()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_search()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_search_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enablers earch service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerSearchSess
                ion) - a ``SequenceRuleEnablerSearchSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_search()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_search()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_admin_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler administration service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerAdminSessi
                on) - a ``SequenceRuleEnablerAdminSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_admin()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_admin()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_admin_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler administration service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerAdminSessi
                on) - a ``SequenceRuleEnablerAdminSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id or proxy is null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_admin()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_admin()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_notification_session(self, sequence_rule_enabler_receiver=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler notification service.

        arg:    sequence_rule_enabler_receiver
                (osid.assessment.authoring.SequenceRuleEnablerReceiver):
                the notification callback
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleEnablerNotificati
                onSession) - a
                ``SequenceRuleEnablerNotificationSession``
        raise:  NullArgument - ``sequence_rule_enabler_receiver`` or
                ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_notification()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_notification()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_notification_session_for_bank(self, sequence_rule_enabler_receiver=None, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler notification service for the given bank.

        arg:    sequence_rule_enabler_receiver
                (osid.assessment.authoring.SequenceRuleEnablerReceiver):
                the notification callback
        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleEnablerNotificati
                onSession) - a
                ``SequenceRuleEnablerNotificationSession``
        raise:  NotFound - no bank found by the given ``Id``
        raise:  NullArgument - ``sequence_rule_enabler_receiver,
                bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_notification()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_notification()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if sequence_rule_enabler_receiver is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_bank_session(self, proxy=None):
        """Gets the ``OsidSession`` to lookup sequence rule enabler/bank mappings for sequence rule enablers.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerBankSessio
                n) - a ``SequenceRuleEnablerBankSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_bank()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_bank_assignment_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with assigning sequence rule enablers to bank.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleEnablerBankAssign
                mentSession) - a
                ``SequenceRuleEnablerBankAssignmentSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_bank_assignment()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_bank_assignment()`` is
        ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_smart_bank_session(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` to manage sequence rule enabler smart bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerSmartBankS
                ession) - a ``SequenceRuleEnablerSmartBankSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_smart_bank()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_smart_bank()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_lookup_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler mapping lookup service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerRuleLookup
                Session) - a ``SequenceRuleEnablerRuleLookupSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_lookup()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_lookup()`` is ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_lookup_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler mapping lookup service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return:
                (osid.assessment.authoring.SequenceRuleEnablerRuleLookup
                Session) - a ``SequenceRuleEnablerRuleLookupSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_lookup()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_lookup()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_application_session(self, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler assignment service.

        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleEnablerRuleApplic
                ationSession) - a
                ``SequenceRuleEnablerRuleApplicationSession``
        raise:  NullArgument - ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_application()`` is
                ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_application()`` is
        ``true``.*

        """
        if proxy is None:
            raise NullArgument()
        raise Unimplemented()

    def get_sequence_rule_enabler_rule_application_session_for_bank(self, bank_id=None, proxy=None):
        """Gets the ``OsidSession`` associated with the sequence rule enabler assignment service for the given bank.

        arg:    bank_id (osid.id.Id): the ``Id`` of the ``Bank``
        arg:    proxy (osid.proxy.Proxy): a proxy
        return: (osid.assessment.authoring.SequenceRuleEnablerRuleApplic
                ationSession) - a
                ``SequenceRuleEnablerRuleApplicationSession``
        raise:  NotFound - no ``Bank`` found by the given ``Id``
        raise:  NullArgument - ``bank_id`` or ``proxy`` is ``null``
        raise:  OperationFailed - unable to complete request
        raise:  Unimplemented -
                ``supports_sequence_rule_enabler_rule_application()`` or
                ``supports_visible_federation()`` is ``false``
        *compliance: optional -- This method must be implemented if
        ``supports_sequence_rule_enabler_rule_application()`` and
        ``supports_visible_federation()`` are ``true``.*

        """
        if bank_id is None or proxy is None:
            raise NullArgument
        raise Unimplemented()
