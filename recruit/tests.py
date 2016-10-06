from basket_together.views import index
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase


class IndexPageTest(TestCase):

    def test_root_url_resolves_to_index_page(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.strip().startswith(b'<html>'))
        self.assertIn(b'<title>Basket Together</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))