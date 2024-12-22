"""
models.py is responsible for the creation of the custom user models and links to the database. 

"""


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom manager for user creation
class CustomUserManager(BaseUserManager):
    """
    Model for the creation of superuser. Only ONE SUPERUSER must be created, but can be used by anyone
    on the developer team. Superuser handles both the admin and student accounts
    """
    def create_user(self, email, password=None, **extra_fields):
        # Ensure email is provided
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize email (convert to lowercase)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Ensure only one superuser exists
        if CustomUser.objects.filter(role='superuser').exists():
            raise ValueError("A superuser already exists!")
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = 'superuser'
        
        # Restrict superuser fields
        if any(field in extra_fields for field in ['acad_year', 'acad_block', 'membership_id', 'student_id']):
            raise ValueError("Superuser cannot have academic or membership information.")
        
        return self.create_user(email, password, **extra_fields)



# Custom user model extending AbstractBaseUser
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    This is the model for the account creation. Since it inherits AbstractBaseUser, it naturally
    possesses AUTHENTICATION SYSTEM, including password hashing, ID tagging, and log-in credentials.

    Note: These models must be migrated to the database FIRST, before creating any tables, to ensure
    that the foreign keys are connected properly.
    
    """
    email = models.EmailField(unique=True)  # Use email as unique identifier
    given_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, default='student')  # 'student' or 'admin'
    acad_year = models.IntegerField(null=True, blank=True)
    acad_block = models.CharField(max_length=1, null=True, blank=True)
    membership_id = models.CharField(max_length=20, null=True, blank=True)
    student_id = models.CharField(max_length=10, null=True, blank=True)
    user_password = models.CharField(max_length=255)  # Password field (hashed)

    is_staff = models.BooleanField(default=False)  # Add the is_staff field here
    is_active = models.BooleanField(default=True)  # Optional: Add is_active for active users


    # Set the custom manager for user creation
    objects = CustomUserManager()

    # Tell Django to use the email field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['given_name', 'last_name']  # Fields required during registration

    def __str__(self):
        return f'{self.given_name} {self.last_name}'  # String representation of the user
