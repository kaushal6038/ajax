from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = 'testapp.admin.MyAdminSite'

class TestappConfig(AppConfig):
    name = 'testapp'
