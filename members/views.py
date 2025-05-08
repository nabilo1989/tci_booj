from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'حساب کاربری با موفقیت ایجاد شد!')
            return redirect('contact_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'members/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید!')
                next_url = request.POST.get('next', 'contact_list')
                return redirect(next_url)
        # اگر فرم معتبر نباشد، خود فرم پیام‌های خطا را دارد
    else:
        form = LoginForm(request)

    return render(request, 'members/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید!')
    return redirect('contact_list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def verify_user(request, user_id):
    user_to_verify = CustomUser.objects.get(id=user_id)
    user_to_verify.is_verified = True
    user_to_verify.verified_by = request.user
    user_to_verify.save()
    messages.success(request, f'کاربر {user_to_verify.username} تایید شد')
    return redirect('user_management')


@login_required
def user_management(request):
    if not request.user.is_superuser:
        return redirect('home')

    unverified_users = CustomUser.objects.filter(is_verified=False)
    context = {'unverified_users': unverified_users}
    return render(request, 'members/user_management.html', context)

@login_required
def permission_denied_view(request, exception=None):
    return render(request, './members/403.html', status=403)

@login_required
def profile_view(request):
    return render(request, 'members/profile.html')