from .models import Photo
from rest_framework import serializers


class PhotoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo', 'price', 'detail', 'date', 'lat', 'lng', 'address', 'country')

