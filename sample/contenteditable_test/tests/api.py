from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse

from sample.newspaper.models import Article


class BaseTestCase(TestCase):
    fixtures = ['test_auth.json']

    def setUp(self):
        self.obj = Article.objects.get(pk=1)
        self.url = reverse('dce_endpoint')
        self.base_data = {'model': 'article', 'pk': '1'}

    def generate(self, updates):
        new_data = self.base_data.copy()
        new_data.update(updates)
        return new_data


class LoggedInTestCase(BaseTestCase):
    def setUp(self):
        super(LoggedInTestCase, self).setUp()
        self.client.login(username='test', password='test')


class HTTPMethods(LoggedInTestCase):
    def test_get_is_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post_is_allowed(self):
        response = self.client.post(self.url, self.base_data)
        self.assertEqual(response.status_code, 200)

    @unittest.expectedFailure
    def test_put_is_allowed(self):
        response = self.client.put(self.url, self.base_data)
        self.assertEqual(response.status_code, 200)

    @unittest.expectedFailure
    def test_delete_is_allowed(self):
        response = self.client.delete(self.url, self.base_data)
        self.assertEqual(response.status_code, 200)


class Updates(LoggedInTestCase):
    def test_can_update_field(self):
        new_title = "Poopity Poop Pooh"
        response = self.client.post(self.url,
                   self.generate({'title': new_title}))
        self.assertEqual(response.status_code, 200)
        obj = Article.objects.get(pk=1)
        self.assertEqual(obj.title, new_title)


class Permissions(BaseTestCase):
    def test_anonymous_is_rejected(self):
        response = self.client.post(self.url, self.base_data)
        self.assertEqual(response.status_code, 403)
        self.client.login(username='test', password='test')
        response = self.client.post(self.url, self.base_data)
        self.assertEqual(response.status_code, 200)
