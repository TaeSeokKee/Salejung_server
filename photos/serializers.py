from .models import Photo
from rest_framework import serializers


class PhotoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('user', 'photo', 'price', 'detail', 'lat', 'lng')

