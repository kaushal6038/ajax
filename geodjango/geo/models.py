from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=20)
	geo_location = gis_models.PointField(srid=4326, null=True,blank=True)
	address = models.CharField(max_length=20)


	def __str__(self):
		return self.name
