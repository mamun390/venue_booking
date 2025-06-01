from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .models import Venue, BookingRequest
from .forms import BookingRequestForm, RegistrationForm

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
            # Notify admin of new booking request
            send_mail(
                'New Booking Request',
                f'Booking request for venue "{venue.name}" by {booking.user_name} on {booking.event_date}.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            return render(request, 'booking/booking_success.html', {'booking': booking})
    else:
        form = BookingRequestForm()
    return render(request, 'booking/booking_request.html', {'venue': venue, 'form': form})

@staff_member_required
def admin_dashboard(request):
    # List all booking requests for admin approval
    bookings = BookingRequest.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(BookingRequest, pk=booking_id)
        if action == 'approve':
            booking.is_approved = True
            booking.save()
            # Notify user of approval
            send_mail(
                'Booking Approved',
                f'Your booking for venue "{booking.venue.name}" on {booking.event_date} has been approved.',
                settings.DEFAULT_FROM_EMAIL,
                [booking.user_email],
                fail_silently=True,
            )
        elif action == 'unapprove':
            booking.is_approved = False
            booking.save()
        return redirect('booking:admin_dashboard')
    
    return render(request, 'booking/admin_dashboard.html', {'bookings': bookings})

def user_dashboard(request):
    user_email = request.GET.get('email')
    if not user_email:
        return redirect('booking:venue_list')
    
    pending_requests = BookingRequest.objects.filter(user_email=user_email, is_approved=False)
    approved_bookings = BookingRequest.objects.filter(user_email=user_email, is_approved=True)
    
    return render(request, 'booking/user_dashboard.html', {
        'pending_requests': pending_requests,
        'approved_bookings': approved_bookings,
    })

def registration(request, booking_id):
    booking = get_object_or_404(BookingRequest, pk=booking_id, is_approved=True)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=booking)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.is_registered = True
            reg.is_paid = True  # Assuming registration confirms payment; adjust if needed
            reg.save()
            # Optionally notify user/admin about completed registration here
            return render(request, 'booking/registration_success.html', {'booking': booking})
    else:
        form = RegistrationForm(instance=booking)
    return render(request, 'booking/registration_form.html', {'form': form, 'booking': booking})
