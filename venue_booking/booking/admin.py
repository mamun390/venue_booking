from django.contrib import admin
from .models import Venue, BookingRequest

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'venue', 'event_date', 'start_time', 'end_time', 'is_approved', 'is_paid')
    list_filter = ('is_approved', 'is_paid', 'event_date')
    search_fields = ('user_name', 'user_email', 'venue__name')
