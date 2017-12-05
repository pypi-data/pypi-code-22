# coding: utf-8

"""
    DocuSign REST API

    The DocuSign REST API provides you with a powerful, convenient, and simple Web services API for interacting with DocuSign.

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import docusign_esign
from docusign_esign.rest import ApiException
from docusign_esign.models.template_role import TemplateRole


class TestTemplateRole(unittest.TestCase):
    """ TemplateRole unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplateRole(self):
        """
        Test TemplateRole
        """
        model = docusign_esign.models.template_role.TemplateRole()


if __name__ == '__main__':
    unittest.main()
