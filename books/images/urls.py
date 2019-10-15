from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^clear/$', clear_database, name='clear_database'),
    url(r'^simple/$', simple_upload, name='simple_upload'),
    url(r'^progress-bar-upload/$', ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'^model_form_upload/$', model_form_upload.as_view(), name='model_form_upload'),
]