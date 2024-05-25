from django.test import TestCase
from products_app.models import Product, Historical
from django.utils import timezone

class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(ticker='BTC-USD', name='Bitcoin')

    def test_product_creation(self):
        self.assertEqual(self.product.ticker, 'BTC-USD')
        self.assertEqual(self.product.name, 'Bitcoin')
        self.assertEqual(str(self.product), 'Bitcoin (BTC-USD)')

class HistoricalModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(ticker='BTC-USD', name='Bitcoin')
        self.timestamp = timezone.now()
        self.historical = Historical.objects.create(
            product=self.product,
            timestamp=self.timestamp,
            open=30000.0,
            high=31000.0,
            low=29500.0,
            close=30500.0
        )

    def test_historical_creation(self):
        self.assertEqual(self.historical.product, self.product)
        self.assertEqual(self.historical.timestamp, self.timestamp)
        self.assertEqual(self.historical.open, 30000.0)
        self.assertEqual(self.historical.high, 31000.0)
        self.assertEqual(self.historical.low, 29500.0)
        self.assertEqual(self.historical.close, 30500.0)
        self.assertEqual(str(self.historical), f'{self.product.ticker} at {self.timestamp}')
