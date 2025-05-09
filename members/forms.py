from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_verified = False  # کاربر جدید به صورت پیش‌فرض تایید نشده
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری یا ایمیل'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'کلمه عبور'
        })
    )





class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='ایمیل')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="شماره تلفن باید به این فرمت وارد شود: '+999999999'")
    phone = forms.CharField(validators=[phone_regex], max_length=17, required=False, label='تلفن همراه')

    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'national_id', 'gender', 'birth_date', 'address', 'bio', 'website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'avatar': 'تصویر پروفایل',
            'national_id': 'کد ملی',
            'gender': 'جنسیت',
            'birth_date': 'تاریخ تولد',
            'address': 'آدرس',
            'bio': 'درباره من',
            'website': 'وبسایت',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }