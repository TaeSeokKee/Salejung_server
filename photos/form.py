from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('userId', 'photo', 'price', 'detail', 'date', 'lat', 'lng', 'address', 'country', 'topic', )
