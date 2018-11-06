from django.db import models

class ProductData(models.Model):
    product_id = models.IntegerField(default=1)
    sales = models.IntegerField()
    rating = models.CharField(max_length=50)
    price_cents = models.IntegerField()
    trending = models.BooleanField()
    scrape_time = models.CharField(max_length=30)
    updated_at = models.CharField(max_length=30)
    site = models.CharField(max_length=30)