# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
class RoutesTest(TestCase):

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_profile(self):
        resp = self.client.get('/profile/')
        self.assertNotEqual(resp.status_code, 200)
        self.assertEqual(resp.status_code, 302)

    def test_categories(self):
        resp = self.client.get('/category/')
        self.assertEqual(resp.status_code, 200)

    def test_category_details(self):
        resp = self.client.get('/category/2')
        self.assertEqual(resp.status_code, 301)
