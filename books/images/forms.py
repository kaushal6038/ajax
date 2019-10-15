from django import forms

from .models import *


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )