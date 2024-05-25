import requests
from .models import Product


def is_valid_ticker(ticker):
    url = 'https://api.exchange.coinbase.com/products'
    headers = {
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return False

    products = response.json()
    for product in products:
        if product['id'] == ticker:
            return True
    return False


def fetch_candle_data(product_id, start, end, granularity=3600):
    product = Product.objects.get(id=product_id)
    url = f'https://api.exchange.coinbase.com/products/{product.ticker}/candles'
    params = {
        'start': start.isoformat(),
        'end': end.isoformat(),
        'granularity': granularity
    }
    response = requests.get(url, params=params)
    return response.json()

