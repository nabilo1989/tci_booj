from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def verified_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('members:login')

        if not request.user.is_verified and not request.user.is_superuser:
            return redirect('members:permission_denied')  # حالا این URL تعریف شده است

        return view_func(request, *args, **kwargs)

    return wrapper