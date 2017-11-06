from django.db import models

# Create your models here.

# Todo : image upload path will be specific date.
class Photo(models.Model):
    user = models.CharField(max_length=50, blank=False)
    photo = models.ImageField(upload_to='.', default='')
    price = models.IntegerField(blank=False)
    detail = models.CharField(max_length=100, blank=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['lat', 'lng'])
        ]

