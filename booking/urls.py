from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('venue/<int:venue_id>/book/', views.booking_request, name='booking_request'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking/<int:booking_id>/register/', views.registration, name='registration'),
]
