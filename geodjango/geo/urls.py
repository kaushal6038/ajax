from django.urls import path
from .views import (details,current_location,buyer_location,nearest_stores,stores_list)

urlpatterns = [
    path('',details),
    path('save-detail',current_location),

    path('user',buyer_location),
    path('nearest_stores',nearest_stores),

    path('stores',stores_list),
]
