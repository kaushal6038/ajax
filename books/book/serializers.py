from rest_framework import serializers
from .models import *

class PersonSerializer(serializers.ModelSerializer):
	country = serializers.SerializerMethodField()
	city = serializers.SerializerMethodField()

	class Meta:
		model = Person
		fields = ['name','birthdate','country','city']


	def get_country(self, obj):
		return obj.country.name


	def get_city(self, obj):
		return obj.city.name