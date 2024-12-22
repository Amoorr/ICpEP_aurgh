"""
URL configuration for ICpEP_Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', acc_views.student_login, name='student_login'),  # Student login
    path('custom_admin/login/', acc_views.admin_login, name='admin_login'),  # Admin login
    path('student_dashboard/', acc_views.student_dashboard, name='student_dashboard'),  # URL for student dashboard
    path('admin_dashboard/', acc_views.admin_dashboard, name='admin_dashboard'),  # URL for admin dashboard
    path('', include('accounts.urls')),  # Include other URLs from the accounts app (if any)
    path('marketplace/', include('marketplace.urls')),  # Include the marketplace app URLs
    path('calendar/', include(('event_calendar.urls', 'event_calendar'), namespace='event_calendar')),
    path('news/', include(('news.urls', 'news'), namespace='news')),

]

from django.conf import settings
from django.conf.urls.static import static

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

