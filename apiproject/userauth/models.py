from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class CustomUser(AbstractUser):
	name = models.CharField(blank=True, max_length=255)

	def __str__(self):
		return self.email

class UserOtp(models.Model):
	email = models.EmailField(max_length=50)

	def __str__(self):
		return self.email

class MyCustomAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        email = request.GET.get("email")

        if not email: # no username passed in request headers
            return None # authentication did not succeed

        try:
            user = UserOtp.objects.get(email=email) # get the user
        except UserOtp.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist

        return (user, None) # authentication successful
