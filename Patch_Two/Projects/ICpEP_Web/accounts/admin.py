from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

"""
For admin interface only. Can be ignored.

"""

# Define the custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'given_name', 'last_name', 'role', 'is_staff', 'is_superuser')  # Fields to display in the list view
    list_filter = ('role', 'is_staff', 'is_superuser')  # Filters to apply in the list view
    search_fields = ('email', 'given_name', 'last_name')  # Fields to search by
    ordering = ('email',)  # Default ordering

    # Fields to display in the user creation and change forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('given_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('given_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    # Ensure the password is hashed properly and the user is active
    def save_model(self, request, obj, form, change):
        if not obj.password:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
