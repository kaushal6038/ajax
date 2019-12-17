from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import *
# Register your models here

class MyAdminSite(AdminSite):
	site_header = "Test Header"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('image','admin_image')


admin_site = MyAdminSite(name='myadmin')
admin_site.register(MyModel)
admin_site.register(Modeltest, ArticleAdmin)
