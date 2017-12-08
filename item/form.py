from django import forms
from .models import Item

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = (
            'userId', 
        	'photoFilePath', 
        	'name',
            'price',
        	'date', 
        	'lat', 
        	'lng', 
        	'address', 
        	'country',
        	'channelUrl',
            'category', 
            'detail',
            'isClosed',
            )
