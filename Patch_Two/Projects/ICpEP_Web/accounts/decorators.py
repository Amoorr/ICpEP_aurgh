from functools import wraps
from django.shortcuts import redirect

def role_required(required_role):
    """
    How to Use:

        If you want a view (on views.py) to be accessed only by admins, put this decorator
    on top of the function:

        @role_required('admin')

        The same goes with:

        @role_required('student')

        This is to ensure that admins and students can access their corresponding pages.
    
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in required_role:
                return view_func(request, *args, **kwargs)
            # Redirect to login or error page if unauthorized
            return redirect('student_login')  # or replace 'login' with an error page name
        return _wrapped_view
    return decorator
from functools import wraps
from django.http import HttpResponseForbidden

