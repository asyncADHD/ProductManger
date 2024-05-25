from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.utils import timezone
from products_app.models import Product, Historical
from products_app.tasks import fetch_and_store_candle_data
import datetime

class FetchAndStoreCandleDataTests(TestCase):

    def setUp(self):
        self.product1 = Product.objects.create(name='Test Product 1', ticker='BTC-USD')
        self.product2 = Product.objects.create(name='Test Product 2', ticker='ETH-USD')

    @patch('products_app.tasks.requests.get')
    def test_fetch_and_store_candle_data(self, mock_get):
        # Mock response data
        mock_response_data = [
            [int((timezone.now() - datetime.timedelta(hours=1)).timestamp()), 30000.0, 31000.0, 30500.0, 30800.0],
            [int((timezone.now() - datetime.timedelta(hours=2)).timestamp()), 29500.0, 30500.0, 30000.0, 30200.0],
        ]

        # Mock the requests.get() method
        mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=mock_response_data))

        # Call the task
        result = fetch_and_store_candle_data()

        # Verify the Historical objects were created
        self.assertEqual(Historical.objects.count(), 4)  # 2 entries for each product
        for entry in mock_response_data:
            timestamp = timezone.make_aware(datetime.datetime.fromtimestamp(entry[0]))
            self.assertTrue(Historical.objects.filter(
                product=self.product1,
                timestamp=timestamp,
                low=entry[1],
                high=entry[2],
                open=entry[3],
                close=entry[4]
            ).exists())
            self.assertTrue(Historical.objects.filter(
                product=self.product2,
                timestamp=timestamp,
                low=entry[1],
                high=entry[2],
                open=entry[3],
                close=entry[4]
            ).exists())

        self.assertEqual(result, "Data fetched and stored for all tickers")


