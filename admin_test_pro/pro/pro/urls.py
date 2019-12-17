from testapp.admin import admin_site
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin_site.urls),
    path('',include('testapp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
