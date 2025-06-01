from django.db import models
from django.utils import timezone

class Venue(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='venues/')
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

class BookingRequest(models.Model):
    PAYMENT_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    message = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Registration related fields
    registration_name = models.CharField(max_length=100, blank=True, null=True)
    registration_nid = models.CharField(max_length=30, blank=True, null=True)
    registration_phone = models.CharField(max_length=20, blank=True, null=True)
    registration_email = models.EmailField(blank=True, null=True)
    registration_cause = models.TextField(blank=True, null=True)
    payment_system = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} - {self.venue.name} on {self.event_date}"
