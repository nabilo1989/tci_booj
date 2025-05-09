from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .forms import ProfileForm,CustomUser,Profile

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

# @login_required
# def profile_view(request):
#     return render(request, 'members/profile.html')



@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'profile': user.profile  # اگر مدل Profile دارید
    }
    return render(request, 'members/profile.html', context)




@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به‌روزرسانی شد!')
            return redirect('members:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'members/profile.html', context)





@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد')
            return redirect('members:profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'members/edit_profile.html', {'form': form})