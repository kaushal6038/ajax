from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,UserOtp



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','name',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class EmailForm(forms.ModelForm):
	class Meta:
		model = UserOtp
		fields = ('email',	)

class OtpForm(forms.Form):
    email = forms.EmailField(max_length=40)
    otp = forms.CharField(max_length=6,widget=forms.TextInput(attrs={'pattern':'[0-9]+','title':'Enter numbers Only '}))

