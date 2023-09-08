from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def reviewer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Reviewer').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('reviews:index')  # Redirect users who are not reviewers
    return login_required(_wrapped_view)
