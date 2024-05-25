from django.db import models


class Product(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class Historical(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()

    def __str__(self):
        return f"{self.product.ticker} at {self.timestamp}"
