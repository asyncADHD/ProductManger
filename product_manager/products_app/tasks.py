from celery import shared_task
from django.utils import timezone
import requests
from .models import Product, Historical
import datetime


@shared_task
def fetch_and_store_candle_data():
    granularity = 3600  # One hour granularity  =3600

    # Fetch all products/tickers from the database
    products = Product.objects.all()

    for product in products:
        url = f'https://api.exchange.coinbase.com/products/{product.ticker}/candles?granularity={granularity}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            historical_data = [
                Historical(
                    product=product,
                    timestamp=timezone.make_aware(datetime.datetime.fromtimestamp(entry[0])),
                    low=entry[1],
                    high=entry[2],
                    open=entry[3],
                    close=entry[4]
                )
                for entry in data
            ]
            Historical.objects.bulk_create(historical_data)

        else:
            print(f"Failed to fetch data for {product.ticker}")

    return "Data fetched and stored for all tickers"
