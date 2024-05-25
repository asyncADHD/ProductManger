from django.test import SimpleTestCase
from django.urls import reverse, resolve
from products_app.views import (home, product_list, product_create, product_update, product_delete, price_history, get_historical_data)

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_product_list_url_is_resolved(self):
        url = reverse('product_list')
        self.assertEqual(resolve(url).func, product_list)

    def test_product_create_url_is_resolved(self):
        url = reverse('product_create')
        self.assertEqual(resolve(url).func, product_create)

    def test_product_update_url_is_resolved(self):
        url = reverse('product_update', args=[1])
        self.assertEqual(resolve(url).func, product_update)

    def test_product_delete_url_is_resolved(self):
        url = reverse('product_delete', args=[1])
        self.assertEqual(resolve(url).func, product_delete)

    def test_price_history_url_is_resolved(self):
        url = reverse('price_history')
        self.assertEqual(resolve(url).func, price_history)

    def test_get_historical_data_url_is_resolved(self):
        url = reverse('historical_data', args=[1])
        self.assertEqual(resolve(url).func, get_historical_data)
