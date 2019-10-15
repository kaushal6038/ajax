from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.create_book_normal,name='users'),
    path('book/list', views.BookListView.as_view(), name='book_list'),
 
    ]