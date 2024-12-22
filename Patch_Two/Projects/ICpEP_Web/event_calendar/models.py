from django.db import models
from accounts.models import CustomUser  # Assuming the CustomUser model is in the accounts app


# Event model: Stores information about events
class Event(models.Model):
    EVENT_TAGS = [
        ('General', 'General'),
        ('Organizational', 'Organizational'),
    ]

    event_id = models.AutoField(primary_key=True)  # Explicitly defining the primary key as event_id
    event_name = models.CharField(max_length=200)
    event_tag = models.CharField(
        max_length=20, choices=EVENT_TAGS, default='General'
    )
    event_venue = models.CharField(max_length=200, null=True, blank=True)  # Add venue field
    needs_attendance = models.BooleanField(default=False)
    event_date = models.DateField()
    event_time = models.TimeField()
    

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'Event'  # Custom table name if needed, otherwise defaults to the model name in lowercase
        ordering = ['event_date', 'event_time']  # Orders events by date and time

        
# Attendance Span model: Tracks the start and end times for attendance
class AttendanceSpan(models.Model):
    attendance_span_id = models.AutoField(primary_key=True)  # Explicitly defining the primary key as event_id
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='event_id')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.event.event_name} Attendance Span"

    class Meta:
        db_table = 'Attendance_Span'  # Custom table name, could be left out if it matches convention
        ordering = ['start_date', 'start_time']  # Orders spans by start date and time


# Participation model: Tracks user participation in events (attendance state)
class Participation(models.Model):
    PARTICIPATION_STATE = [
        ('Absent', 'Absent'),
        ('Present', 'Present'),
        ('Partial Present', 'Partial Present'),
    ]

    participation_id = models.AutoField(primary_key=True)  # Explicitly defining the primary key as event_id
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='event_id')
    admin = models.ForeignKey(CustomUser, related_name='admin_participation', on_delete=models.CASCADE)
    event_state = models.CharField(max_length=20, choices=PARTICIPATION_STATE, default='Absent')
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.given_name} {self.user.last_name} - {self.event.event_name} ({self.event_state})"

    class Meta:
        db_table = 'Participation'  # Custom table name
        unique_together = ['user_id', 'event_id']  # Ensures each user can participate in an event only once
        ordering = ['event_id']  # Orders participation by event date and time

class ScanData(models.Model):
    scanned_text = models.TextField()  # Store the scanned text
    scanned_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the scan was made

    def __str__(self):
        return f"Scanned at {self.scanned_at} - {self.scanned_text[:50]}"