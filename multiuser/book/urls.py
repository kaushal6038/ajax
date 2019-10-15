from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    # path('', views.person_list_view, name='person_list'),
    path('email/',views.email),
    
    path('teachers/',views.teachers,name='teachers'),
    path('classes/',views.list_of_classes,name='classes'),
    path('students/<int:pk>',views.listOfStudents,name='students'),
    path('class-add/',views.classAdd,name='classAdd'),

    path('person/',views.person_list_pagination,name='person_list'),
    path('person-ajax',views.person_list_ajax),
    path('ssession',views.setsession), 

    path('gsession',views.getsession),
    path('person_create/', views.PersonCreateView, name='person_add'),
    path('ajax-list',views.person_list),
    path('ajax-load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here




    path('list',views.person_list,name='person'),
    path('csv',views.csv_file,name='csv'),
    path('pdf',views.GeneratePDF,name='pdf'),
    path('doc',views.GenerateDoc,name='pdf'),
]