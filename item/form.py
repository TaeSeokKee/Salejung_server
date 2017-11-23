from django import forms
from .models import Item

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = (
            '_id',
            'userId', 
        	'photoFilePath', 
        	'name',
            'price',
        	'date', 
        	'lat', 
        	'lng', 
        	'address', 
        	'country', 
        	'topic', 
        	'channelUrl', 
            )
