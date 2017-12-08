from .models import Item
from rest_framework import serializers


class GetItemsInfoByLngLatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'photoFilePath', 'name', 'channelUrl', 'price', 'detail', )


class GetItemsLocationByLngLatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('lng', 'lat', )


class GetItemByIdForRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'userId', )


class GetItemByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'photoFilePath', 'name', 'price', 'lng', 'lat',)


