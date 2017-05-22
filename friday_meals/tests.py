# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.core import mail
from friday_meals.models import User

class RoutesTest(TestCase):
    fixtures = ['users.json', 'categories.json', 'meals.json']

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.post('/login/', {'email':'donald@ss.eu', 'password':'asdasdasd'}, follow=True)
        self.assertTrue(resp.status_code, 302)
        self.assertIn('/', resp.redirect_chain[0][0])
        self.assertEqual(resp.context['title'], 'Profile')

    def test_profile(self):
        resp = self.client.get('/profile/')
        self.assertNotEqual(resp.status_code, 200)
        self.assertEqual(resp.status_code, 302)
        # Make a Login request
        self.client.login(email='donald@ss.eu', password='asdasdasd')
        resp3 = self.client.get('/profile/')
        self.assertEqual(resp3.status_code, 200)

    def test_admin_panel(self):
        resp = self.client.get('/admin_panel/', follow=True)
        self.assertEqual(resp.status_code, 200)
        string = str(resp.redirect_chain)
        lst = string.split('/')
        self.assertIn('?next=', lst)
        self.assertIn('admin_panel', lst)

    def test_categories(self):
        resp = self.client.get('/category/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Десерти', [category.title for category in resp.context['categories']])

    def test_category_id(self):
        resp = self.client.get('/category/2/')
        self.assertEqual(resp.context['category'].title, 'Сендвичи') # Ensure category title is correct
        resp2 = self.client.get('/category/321/')
        self.assertEqual(resp2.status_code, 302) # If No such category - the view redirects to 'all_categories'

    def test_meal(self):
        resp = self.client.get('/meal/23/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['meal'].title, 'Мешани сирења')
        self.assertEqual(resp.context['meal'].category.title, 'Ладно мезе' )







    def test_send_mail(self):
        mail.send_mail(
            'Subject line',
            "Body text",
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject line')
