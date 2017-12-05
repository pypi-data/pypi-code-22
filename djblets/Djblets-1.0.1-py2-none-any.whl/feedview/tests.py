#
# tests.py -- Unit tests for classes in djblets.feedview
#
# Copyright (c) 2008  Christian Hammond
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

from django.test.utils import override_settings

from djblets.testing.testcases import TestCase


@override_settings(ROOT_URLCONF='djblets.feedview.test_urls')
class FeedViewTests(TestCase):
    def testViewFeedPage(self):
        """Testing view_feed with the feed-page.html template"""
        response = self.client.get('/feed/')
        self.assertContains(response, "Django 1.0 alpha released", 1)
        self.assertContains(response, "Introducing Review Board News", 1)

    def testViewFeedInline(self):
        """Testing view_feed with the feed-inline.html template"""
        response = self.client.get('/feed-inline/')
        self.assertContains(response, "Django 1.0 alpha released", 1)
        self.assertContains(response, "Introducing Review Board News", 1)

    def testViewFeedError(self):
        """Testing view_feed with a URL error"""
        response = self.client.get('/feed-error/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error' in response.context)
