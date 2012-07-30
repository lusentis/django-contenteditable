from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse

# from sample.newspaper.models import Article


class HTTPMethodsTestCase(TestCase):
    fixtures = ['test_auth.json']

    def test_get_is_not_allowed(self):
        url = reverse('dce_endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_post_is_allowed(self):
        url = reverse('dce_endpoint')
        self.client.login(username='test', password='test')
        response = self.client.post(url, {'model': 'article', 'pk': '1'})
        self.assertEqual(response.status_code, 200)

    @unittest.expectedFailure
    def test_put_is_allowed(self):
        url = reverse('dce_endpoint')
        self.client.login(username='test', password='test')
        response = self.client.put(url, {'model': 'article', 'pk': '1'})
        self.assertEqual(response.status_code, 200)

    @unittest.expectedFailure
    def test_delete_is_allowed(self):
        url = reverse('dce_endpoint')
        self.client.login(username='test', password='test')
        response = self.client.delete(url, {'model': 'article', 'pk': '1'})
        self.assertEqual(response.status_code, 200)
