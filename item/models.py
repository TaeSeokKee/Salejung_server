from django.db import models

# Create your models here.

# Todo : image upload path will be specific date.
class Item(models.Model):
    userId = models.CharField(max_length=50, blank=False)
    photoFilePath = models.TextField(max_length=200, blank=False)
    name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(blank=False)
    date = models.CharField(max_length=20, blank=False)
    lat = models.DecimalField(max_digits=12, decimal_places=9, blank=False)
    lng = models.DecimalField(max_digits=12, decimal_places=9, blank=False)
    address = models.TextField(max_length=100, blank=False)
    country = models.CharField(max_length=10, blank=False)
    channelUrl = models.TextField(max_length=200, blank=False)
    category = models.CharField(max_length=50, blank=True)
    detail = models.TextField(max_length=200, blank=True)
    isClosed= models.BooleanField(default=False, blank=True)
    # isBadUser= models.BooleanField(default=False, blank=True)
    # stars= models.IntegerField(default=0, blank=True)

    class Meta:
        # lng index and next lat index is more efficient.
        indexes = [
            models.Index(fields=['lng', 'lat', ]),
            models.Index(fields=['userId']),
        ]

