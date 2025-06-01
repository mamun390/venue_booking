from django import forms
from .models import BookingRequest

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['user_name', 'user_email', 'event_date', 'start_time', 'end_time', 'message']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = [
            'registration_name',
            'registration_nid',
            'registration_phone',
            'registration_email',
            'registration_cause',
            'payment_system',
        ]
        widgets = {
            'registration_cause': forms.Textarea(attrs={'rows': 3}),
            'payment_system': forms.Select(),
        }
