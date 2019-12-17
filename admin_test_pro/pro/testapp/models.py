from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
class MyModel(models.Model):
	name = models.CharField(max_length=20)

	class Meta:
		verbose_name = "My Test Model"

class Modeltest(models.Model):
    image = models.ImageField(upload_to='picture')
    
    def admin_image(self):
        return mark_safe('<img src={} height="42" width="42"> '.format(self.image.url))
    admin_image.allow_tags = True