from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('user', 'photo', 'price', 'detail', 'date', 'lat', 'lng', 'address',)


