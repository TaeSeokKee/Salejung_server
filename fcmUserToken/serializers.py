from .models import FcmUserToken
from rest_framework import serializers


class FcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcmUserToken
        fields = ('userId', 'token', )

