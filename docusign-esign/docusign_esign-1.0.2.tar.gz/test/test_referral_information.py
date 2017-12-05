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
from docusign_esign.models.referral_information import ReferralInformation


class TestReferralInformation(unittest.TestCase):
    """ ReferralInformation unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReferralInformation(self):
        """
        Test ReferralInformation
        """
        model = docusign_esign.models.referral_information.ReferralInformation()


if __name__ == '__main__':
    unittest.main()
