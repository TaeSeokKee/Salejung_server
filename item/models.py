from django.db import models

# Create your models here.

# Todo : image upload path will be specific date.
class Item(models.Model):
    _id = models.CharField(max_length=50, blank=False)
    userId = models.CharField(max_length=50, blank=False)
    photoFilePath = models.TextField(max_length=200, blank=False)
    name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(blank=False)
    date = models.TextField(max_length=100, blank=False)
    lat = models.DecimalField(max_digits=12, decimal_places=9, blank=False)
    lng = models.DecimalField(max_digits=12, decimal_places=9, blank=False)
    address = models.TextField(max_length=100, blank=False)
    country = models.CharField(max_length=10, blank=False)
    topic = models.CharField(max_length=20, blank=False)
    channelUrl = models.TextField(max_length=150, blank=False)


    class Meta:
        # lng index and next lat index is more efficient.
        indexes = [
            models.Index(fields=['lng', 'lat']),
            models.Index(fields=['userId']),
            models.Index(fields=['_id']),
        ]

