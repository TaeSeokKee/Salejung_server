from .models import Photo
from rest_framework import serializers


class GetItemByLngLatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photoFilePath', 'detail', 'date', 'channelUrl', )


class GetItemByUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photoFilePath', 'detail', 'date', 'channelUrl', )

