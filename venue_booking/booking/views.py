from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Venue, BookingRequest
from .forms import BookingRequestForm

def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'booking/venue_list.html', {'venues': venues})

def booking_request(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.venue = venue
            booking.save()
            # Send email notification to admin
            send_mail(
                'New Booking Request',
                f'Booking request for venue "{venue.name}" by {booking.user_name} on {booking.event_date}.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],  # set this in settings.py
                fail_silently=False,
            )
            return render(request, 'booking/booking_success.html', {'booking': booking})
    else:
        form = BookingRequestForm()
    return render(request, 'booking/booking_request.html', {'venue': venue, 'form': form})
