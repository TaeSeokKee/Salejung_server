from django import forms
from .models import FcmUserToken

class FcmUserTokenForm(forms.ModelForm):

    class Meta:
        model = FcmUserToken
        fields = (
            'userId',
            'token',
            )
