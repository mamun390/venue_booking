from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('venue/<int:venue_id>/book/', views.booking_request, name='booking_request'),
]
