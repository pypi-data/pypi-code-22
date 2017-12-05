# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.fhirfield import field
from plone.app.fhirfield.helpers import resource_type_str_to_fhir_model
from plone.app.fhirfield.interfaces import IFhirResourceModel
from plone.app.fhirfield.interfaces import IFhirResourceValue
from plone.app.fhirfield.value import FhirResourceValue
from zope.interface import Invalid
from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
from zope.schema.interfaces import WrongContainedType
from zope.schema.interfaces import WrongType

import json
import os
import six
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class FieldIntegrationTest(unittest.TestCase):
    """ """

    def test_init_validate(self):  # noqa: C901
        """ """
        # Test with minimal params
        try:
            field.FhirResource(
                title=six.text_type('Organization resource')
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))
        # Test with fhir field specific params
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                model='fhirclient.models.organization.Organization',
                model_interface=IFhirResourceModel
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))

        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                resource_type='Organization'
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))

        # resource_type and model are not allowed combinely
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                resource_type='Organization',
                model='fhirclient.models.organization.Organization'
            )
            raise AssertionError('Code should not come here! as should be invalid error')
        except Invalid:
            pass

        # test with invalid pyton style dotted path (fake module)
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                model='fake.fake.models.organization.Organization'
            )
            raise AssertionError('Code should not come here! as should be invalid error')
        except Invalid:
            pass

        # test with invalid fhir model
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                model='plone.app.fhirfield.handler.FhirResourceHandler_'
            )
            raise AssertionError('Code should not come here! as should be invalid error')
        except Invalid as exc:
            self.assertIn('must be valid model class from fhirclient.model', str(exc))

        # test with invalid ResourceType
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                resource_type='FakeResource'
            )
            raise AssertionError('Code should not come here! as should be invalid error')
        except Invalid as exc:
            self.assertIn('FakeResource is not valid resource type', str(exc))

        # Wrong base interface class
        try:
            field.FhirResource(
                title=six.text_type('Organization resource'),
                model_interface=IFhirResourceValue
            )
            raise AssertionError('Code should not come here! as wrong subclass of interface is provided')
        except Invalid:
            pass

    def test_pre_value_validate(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_str = f.read()

        fhir_field = field.FhirResource(title=six.text_type('Organization resource'))

        try:
            fhir_field.pre_value_validate(json_str)
        except Invalid as e:
            raise AssertionError('Code should not come here!\n{0!s}'.format(e))

        fhir_dict = json.loads(json_str)
        resource_type = fhir_dict.pop('resourceType')

        try:
            fhir_field.pre_value_validate(fhir_dict)
            raise AssertionError('Code should not come here! As `resourceType` is not exists.')
        except Invalid:
            pass

        fhir_dict.pop('id')
        fhir_dict['resourceType'] = resource_type
        try:
            fhir_field.pre_value_validate(fhir_dict)
            raise AssertionError('Code should not come here! As `id` is not exists.')
        except Invalid:
            pass

        fhir_dict.pop('resourceType')
        try:
            fhir_field.pre_value_validate(fhir_dict)
            raise AssertionError('Code should not come here! As both `id` and `resourceType` are not exists.')
        except Invalid:
            pass

    def test_validate(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_dict = json.load(f)

        organization = resource_type_str_to_fhir_model('Organization')(json_dict)
        fhir_resource_value = FhirResourceValue(raw=organization)

        fhir_field = field.FhirResource(title=six.text_type('Organization resource'))

        try:
            fhir_field._validate(fhir_resource_value)
        except Invalid as exc:
            raise AssertionError('Code should not come here!\n{0!s}'.format(exc))

        # Test wrong type value!
        try:
            fhir_field._validate(dict(hello='wrong'))
            raise AssertionError('Code should not come here! wrong data type is provide')
        except WrongType as exc:
            self.assertIn('plone.app.fhirfield.value.FhirResourceValue', str(exc))

        type_, address_ = fhir_resource_value.type, fhir_resource_value.address
        fhir_resource_value.type = 390
        fhir_resource_value.address = 'i am wrong type'

        try:
            fhir_field._validate(fhir_resource_value)
            raise AssertionError('Code should not come here! wrong element data type is provided')
        except Invalid as exc:
            self.assertIn('invalid element inside fhir model object', str(exc))

        # Restore
        fhir_resource_value.type = type_
        fhir_resource_value.address = address_
        # Test model constraint
        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            model='fhirclient.models.task.Task'
        )

        try:
            fhir_field._validate(fhir_resource_value)
            raise AssertionError('Code should not come here! model mismatched!')
        except WrongContainedType as exc:
            self.assertIn('Wrong fhir resource value', str(exc))

        # Test resource type constraint!
        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            resource_type='Task'
        )

        try:
            fhir_field._validate(fhir_resource_value)
            raise AssertionError('Code should not come here! model mismatched!')
        except ConstraintNotSatisfied as exc:
            self.assertIn('Resource type must be `Task`', str(exc))

        # Wrong interface attributes
        class IWrongInterface(IFhirResourceModel):
            def meta():
                pass
        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            model_interface=IWrongInterface
        )

        try:
            fhir_field._validate(fhir_resource_value)
            raise AssertionError('Code should not come here! interface and object mismatched!')
        except Invalid as exc:
            self.assertIn('An object does not implement', str(exc))

    def test_from_dict(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_dict = json.load(f)

        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            model='fhirclient.models.organization.Organization'
        )

        try:
            fhir_resource_value = fhir_field.from_dict(json_dict)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid FhirResourceValue.\n{0!s}'.format(exc)
                )

        self.assertEqual(fhir_resource_value.resource_type, json_dict['resourceType'])
        try:
            fhir_resource_value.as_json()
        except Exception:
            raise AssertionError('Code should not come here! as should be valid fhir resource')
        # Test with invalid data type
        try:
            invalid_data = ('hello', 'tree', 'go', )
            fhir_field.from_dict(invalid_data)
        except WrongType as exc:
            self.assertIn('Only dict type data is allowed', str(exc))

        # Test with invalid fhir data
        try:
            invalid_data = dict(hello='fake', foo='bar')
            fhir_field.from_dict(invalid_data)

            raise AssertionError('Code should not come here, because of invalid data')
        except Invalid as exc:
            self.assertIn('Invalid FHIR resource', str(exc))

        # Test contraint
        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            model='fhirclient.models.task.Task'
        )

        try:
            fhir_field.from_dict(json_dict)
            raise AssertionError(
                'Code should not come here as required fhir model is mismatched with provided resourcetype'
            )
        except ConstraintNotSatisfied as exc:
            self.assertIn('Fhir Model mismatched', str(exc))

    def test_fromUnicode(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_str = f.read()

        fhir_field = field.FhirResource(
            title=six.text_type('Organization resource'),
            model='fhirclient.models.organization.Organization'
        )

        try:
            fhir_field.fromUnicode(json_str)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid FhirResourceValue.\n{0!s}'.format(exc)
                )

        # Test with invalid json string
        try:
            invalid_data = '{hekk: invalg, 2:3}'
            fhir_field.fromUnicode(invalid_data)
            raise AssertionError('Code should not come here! invalid json string is provided')
        except Invalid as exc:
            self.assertIn('Invalid JSON String', str(exc))
