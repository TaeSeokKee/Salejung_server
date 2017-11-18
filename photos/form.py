from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('userId', 'photoFilePath', 'detail', 'date', 'lat', 'lng', 'address', 'country', 'topic', )
