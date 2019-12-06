from django import forms
from .models import Location

class PersonForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('__all__')