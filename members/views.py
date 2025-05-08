from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('contact_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'members/signup.html', {'form': form})



# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')  # مطمئن شوید این ریدایرکت کار می‌کند
#         else:
#             # نمایش پیام خطا
#             return render(request, 'members/login.html', {'error': 'نام کاربری یا رمز عبور نادرست'})
#     return render(request, 'members/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or 'contact_list'
            return redirect(next_url)
        else:
            return render(request, 'members/login.html',
                          {'error': 'نام کاربری یا رمز عبور نادرست'})
    return render(request, 'members/login.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید!')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است')
    else:
        form = LoginForm()

    return render(request, 'members/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('contact_list')