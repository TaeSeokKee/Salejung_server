from .models import Item
from rest_framework import serializers


class GetItemInfoByLngLatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('photoFilePath', 'name', 'channelUrl', 'price', )


class GetItemByUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('photoFilePath', 'name', 'date', 'channelUrl', 'price',)


class GetItemLocationByLngLatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('lng', 'lat', )

