"""
URL configuration for phonebook_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # URL‌های احراز هویت
    path('members/password_reset/',
    auth_views.PasswordResetView.as_view(
               template_name='members/password_reset.html',
               email_template_name='members/password_reset_email.html',
               subject_template_name='members/password_reset_subject.txt',
               success_url='password_reset_done'  # اضافه کردن این خط
    ),
           name='password_reset'),

    path('members/password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(
               template_name='members/password_reset_done.html'
    ),
           name='password_reset_done'),

    path('members/reset/<uidb64>/<token>/',
           auth_views.PasswordResetConfirmView.as_view(
               template_name='members/password_reset_confirm.html'
           ),
           name='password_reset_confirm'),

    path('members/reset/done/',
           auth_views.PasswordResetCompleteView.as_view(
               template_name='members/password_reset_complete.html'
           ),
           name='password_reset_complete'),
    path('', include('phonebook.urls')),
    path('members/', include('members.urls')),#,namespace='members'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
