from django.urls import path
from . import views

app_name = 'event_calendar'

urlpatterns = [
    path('admin_calendar/', views.admin_calendar, name='admin_calendar'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/participants/', views.view_participants, name='view_participants'),
    path('student/events/', views.student_calendar, name='student_calendar'),
    path('student/event/<int:event_id>/', views.event_details, name='event_details'),
    path('calendar/event/qr_scanner/<int:event_id>/', views.qr_scanner, name='qr_scanner'),
]
