from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('', views.person_list_view, name='person_list'),
    path('person/',views.person_list_pagination,name='person_list'),
    path('', views.PersonCreateView, name='person_add'),
    path('ajax-list',views.person_list),
    path('ajax-load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here
]