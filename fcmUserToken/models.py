from django.db import models

# Create your models here.
class FcmUserToken(models.Model):
    userId = models.CharField(max_length=50, blank=False, unique=True)
    token = models.TextField(max_length=200, blank=False)

    class Meta:

        indexes = [
            models.Index(fields=['userId']),
        ]