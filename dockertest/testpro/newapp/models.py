from django.db import models

# Create your models here.
class Detail(models.Model):
	name = models.CharField(max_length=20)

	class Meta:
		verbose_name = "Detail"