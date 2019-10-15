from django import forms
from django.forms import formset_factory
from .models import Book


class BookForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )
    number= forms.CharField(label='Number',widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'enter your Number'
        }))

BookFormset = formset_factory(BookForm)


