from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from products_app.models import Product, Historical
import json

class ProductViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(name='Test Product 1', ticker='TP1')
        self.product2 = Product.objects.create(name='Test Product 2', ticker='TP2')
        self.historical1 = Historical.objects.create(product=self.product1, timestamp=timezone.now(), open=100, high=110, low=90, close=105)
        self.historical2 = Historical.objects.create(product=self.product1, timestamp=timezone.now(), open=105, high=115, low=95, close=110)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products_app/product_list.html')
        self.assertIn('page_obj', response.context)
        self.assertIn('total_products', response.context)
        self.assertIn('search_query', response.context)


    def test_product_update_view_post(self):
        response = self.client.post(reverse('product_update', args=[self.product1.pk]), {
            'name': 'Updated Product 1',
            'ticker': 'UP1'
        })
        self.assertEqual(response.status_code, 200)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product 1')
        self.assertEqual(self.product1.ticker, 'UP1')
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.product1.id)
        self.assertEqual(response_data['ticker'], 'UP1')
        self.assertEqual(response_data['name'], 'Updated Product 1')

    def test_product_create_view_invalid_ticker(self):
        response = self.client.post(reverse('product_create'), {
            'name': 'Invalid Product',
            'ticker': 'invalid'
        })
        self.assertEqual(response.status_code, 400)

    def test_product_delete_view(self):
        response = self.client.post(reverse('product_delete', args=[self.product1.pk]))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product1.pk)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products_app/home.html')

    def test_price_history_view(self):
        response = self.client.get(reverse('price_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products_app/price_history.html')
        self.assertIn('products', response.context)
