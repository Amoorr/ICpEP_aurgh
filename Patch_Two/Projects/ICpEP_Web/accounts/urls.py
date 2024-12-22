from django.urls import path
from . import views


"""
urls.py is responsible for mapping the URLs in this 'account' app. 
"""

app_name = 'accounts'

urlpatterns = [
    path('', views.student_login, name='student_login'), # URL line for login
    path('login/', views.student_login, name='student_login'),  # Student login
    path('custom_admin/login/', views.admin_login, name='admin_login'),  # Admin login
    path('register/', views.register, name='register'),  # URL line for registration
    path('accounts/management/', views.admin_accounts, name='admin_accounts'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'), # URL line for student_dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), # URL line for admin_dashboard
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('accounts/list', views.admin_list, name='admin_list'),
    path('accounts/reset_password/<int:user_id>/', views.reset_password, name='admin_reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('accounts/delete/<int:user_id>/', views.admin_delete_account, name='admin_delete_account'),
    path('accounts/edit/<int:user_id>/', views.admin_edit_account, name='admin_edit_account'),
    path('superuser-dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
]