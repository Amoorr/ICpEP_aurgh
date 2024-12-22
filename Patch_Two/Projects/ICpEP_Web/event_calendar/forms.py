from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_tag', 'needs_attendance', 'event_date', 'event_time', 'event_venue']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'event_venue': forms.TextInput(attrs={'class': 'form-control'}),  # Add widget for event_venue
        }
        
from .models import AttendanceSpan

class AttendanceSpanForm(forms.ModelForm):
    class Meta:
        model = AttendanceSpan
        fields = ['start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }