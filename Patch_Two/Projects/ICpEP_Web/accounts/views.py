"""

views.py is responsible for handling the user requests and displaying the corresponding outputs. 

"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, AdminEditAccountForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import role_required
from .models import CustomUser
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render
from event_calendar.models import Event
from news.models import NewsArticle
from accounts.models import CustomUser
from marketplace.models import *
from news.models import *
from event_calendar.models import *
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from marketplace.models import Product, Cart
from event_calendar.models import Event, Participation
from news.models import NewsArticle



# Student login view (default)
def student_login(request):
    """
    Login view for students. It is the default login page.
    Admins will be prevented from logging in here.
    """
    if request.user.is_authenticated:  # Check if the user is already logged in
        # Redirect to respective dashboard based on the user's role
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'superuser':
            return redirect('superuser_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # If the user is an admin, show an error message
                if user.role == 'admin':
                    form.add_error(None, 'Admins should log in using the Admin login page.')
                    return render(request, 'accounts/student_login.html', {'form': form})

                # If the user is a student, log them in
                login(request, user)
                return redirect('student_dashboard')  # Redirect student to their dashboard
            else:
                form.add_error(None, 'Invalid credentials')

    else:
        form = LoginForm()

    return render(request, 'accounts/student_login.html', {'form': form})


# Admin login view
def admin_login(request):
    """
    Login view for admins. Only admins can access this page.
    """
    if request.user.is_authenticated:  # Check if the user is already logged in
        # Redirect to respective dashboard based on the user's role
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'superuser':
            return redirect('superuser_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and user.role == 'admin':  # Ensure only admin can log in here
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Invalid credentials or not an admin account')

    else:
        form = LoginForm()

    return render(request, 'accounts/admin_login.html', {'form': form})

@login_required
@role_required(['admin', 'superuser'])
def register(request):
    """
    Function responsible for registering an account and adding it to the database.
    """

    popup_message = None  # Default: no message
    account_created = False  # Track if an account was created

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            popup_message = 'Account created successfully!'
            form = CustomUserCreationForm()  # Clear the form for the next entry
        else:
            # Aggregate errors into a single message for the pop-up
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(f"{field.capitalize()}: {error}")
            popup_message = " ".join(error_list)  # Combine errors into one message
    else:
        form = CustomUserCreationForm()  # Display an empty form for GET requests

    return render(request, 'accounts/admin/register.html', {
        'form': form,
        'popup_message': popup_message,
    })


@login_required # Decorator where it is only accessed to logged-in users
def logout_view(request):
    """
    Responsible for logging out. Applicable to admins and students
    """
    logout(request)  # Logs out the user
    return redirect('student_login')  # Redirects to the login page


@login_required
@role_required('student') # Custom decorator where it is only accessed by student accounts
def student_dashboard(request):
    """
    Renders the student dashboard
    """
    return render(request, 'accounts/student/student_dashboard.html')

@login_required
@role_required('admin')
def admin_dashboard(request):

    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    active_accounts_count = CustomUser.objects.filter(last_login__gte=thirty_days_ago).count()
    inactive_accounts_count = CustomUser.objects.filter(last_login__lt=thirty_days_ago).count()
    admin_accounts_count = CustomUser.objects.filter(role='admin').count()
    student_accounts_count = CustomUser.objects.filter(role='student').count()

    # 2. Product Summaries
    pre_order_products_count = Product.objects.filter(tag='Pre-orderable').count()
    buyable_products_count = Product.objects.filter(tag='Buyable').count()

    # 3. Net Sales (Orders with 'Received' status)
    net_sales = Cart.objects.filter(order_status='Received').aggregate(total_sales=models.Sum(models.F('quantity') * models.F('product__price')))['total_sales'] or 0

    # 4. Event Summaries
    today = timezone.now().date()
    finished_events_count = Event.objects.filter(event_date__lt=today).count()
    unfinished_events_count = Event.objects.filter(event_date__gte=today).count()
    general_events_count = Event.objects.filter(event_tag='General').count()
    organizational_events_count = Event.objects.filter(event_tag='Organizational').count()

    # 5. News Summary
    total_news = NewsArticle.objects.count()





    products = Product.objects.all()

    query = request.GET.get('search', '')
    news_list = NewsArticle.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else NewsArticle.objects.all()

    events = Event.objects.all()
    now = datetime.now()

    event_data = []
    for event in events:
        attendance_span = AttendanceSpan.objects.filter(event=event).first()
        qr_button_state = "disabled"
        qr_message = "Attendance start time is not yet started."

        if attendance_span:
            start = datetime.combine(attendance_span.start_date, attendance_span.start_time)
            end = datetime.combine(attendance_span.end_date, attendance_span.end_time)

            if start <= now <= end:
                qr_button_state = "enabled"
                qr_message = ""
            elif now > end:
                qr_button_state = "disabled"
                qr_message = "Attendance has already ended."

        event_data.append({
            'event': event,
            'qr_button_state': qr_button_state,
            'qr_message': qr_message,
        })

        users = CustomUser.objects.exclude(role='superuser')

        acad_year_choices = CustomUser.objects.values_list('acad_year', flat=True).distinct()
        acad_block_choices = CustomUser.objects.values_list('acad_block', flat=True).distinct()
        role = CustomUser.objects.values_list('role', flat=True).distinct()


    return render(request, 'accounts/admin/admin_dashboard.html', {
        'products': products,
        'news_list': news_list,
        'events': event_data,
        'users': users,
        'acad_year_choices': acad_year_choices,
        'acad_block_choices': acad_block_choices,
        'role': role,
        'active_accounts': active_accounts_count,
        'inactive_accounts': inactive_accounts_count,
        'admin_accounts': admin_accounts_count,
        'student_accounts': student_accounts_count,
        'pre_order_products': pre_order_products_count,
        'buyable_products': buyable_products_count,
        'net_sales': round(net_sales, 2),
        'finished_events': finished_events_count,
        'unfinished_events': unfinished_events_count,
        'general_events': general_events_count,
        'organizational_events': organizational_events_count,
        'total_news': total_news,
        'current_year': timezone.now().year,
        }) 





@login_required
@role_required(['admin', 'superuser'])
def admin_accounts(request):
    return render(request, 'accounts/admin/admin_accounts.html')

from django.contrib.auth import get_user_model
from django.contrib import messages

@login_required
@role_required(['admin', 'superuser'])
def admin_list(request):
    users = CustomUser.objects.exclude(role = 'superuser')
    
    # Search
    search_term = request.GET.get('search', '')
    if search_term:
        users = users.filter(
            Q(given_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(student_id__icontains=search_term)
        )
    
    # Filter
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    acad_year_filter = request.GET.get('acad_year', '')
    if acad_year_filter:
        users = users.filter(acad_year=acad_year_filter)
    
    acad_block_filter = request.GET.get('acad_block', '')
    if acad_block_filter:
        users = users.filter(acad_block=acad_block_filter)

    # Choices for filtering
    acad_year_choices = CustomUser.objects.values_list('acad_year', flat=True).distinct()
    acad_block_choices = CustomUser.objects.values_list('acad_block', flat=True).distinct()
    role = CustomUser.objects.values_list('role', flat=True).distinct()

    return render(request, 'accounts/admin/admin_list.html', {
        'users': users,
        'acad_year_choices': acad_year_choices,
        'acad_block_choices': acad_block_choices,
        'role': role,  # Pass user role
    })


# Admin view to reset password
@login_required
@role_required(['admin', 'superuser'])
def reset_password(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    user.set_password(user.membership_id)  # Set password to the user's membership ID
    user.save()
    messages.success(request, f'Password for {user.given_name} {user.last_name} has been reset to default.')
    return redirect('admin_list')  # Redirect back to the admin accounts list

@login_required
def change_password(request):
    """
    Handle the password change process for students and admins.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('student_dashboard')  # Redirect to student dashboard after successful change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
@role_required(['admin', 'superuser'])
def admin_delete_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deleting yourself or admins if needed
    if user == request.user:
        messages.error(request, "You cannot delete your own account or admin accounts.")
        return redirect('admin_list')  # Redirect back to the account list
    
    if user.role == 'superuser' and request.user.role != 'superuser':
        messages.error(request, "You do not have permission to edit the superuser account.")
        return redirect('admin_list')

    if user.role == 'superuser':
        messages.error(request, "The main superuser account cannot be deleted.")
        return redirect('admin_list')


    user.delete()
    messages.success(request, f"Account for {user.given_name} {user.last_name} has been deleted.")
    return redirect('admin_list')


from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminEditAccountForm
from .models import CustomUser

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminEditAccountForm
from .models import CustomUser

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminEditAccountForm
from .models import CustomUser

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminEditAccountForm
from .models import CustomUser

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import AdminEditAccountForm
from .models import CustomUser

def admin_edit_account(request, user_id):
    # Get the user to edit using the user_id
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        # Process form data
        form = AdminEditAccountForm(request.POST, instance=user)  # Use the user instance for pre-filling

        if form.is_valid():
            # Save form data
            form.save()

            # Set the success message for the pop-up
            popup_message = "Changes applied successfully!"
            
        else:
            # Set the error message for the pop-up
            popup_message = "Failed to edit account. Please try again."
    else:
        # GET request, show the edit form with existing data
        form = AdminEditAccountForm(instance=user)  # Use the existing user data
        popup_message = None  # No pop-up message on initial GET request

    return render(request, 'accounts/admin/admin_edit_account.html', {
        'form': form,
        'user': user,
        'popup_message': popup_message,  # Pass the pop-up message
    })







@login_required
@role_required('superuser')
def superuser_dashboard(request):
    return render(request, 'accounts/superuser/superuser_dashboard.html')




