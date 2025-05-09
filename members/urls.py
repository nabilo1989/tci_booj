from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'members'

urlpatterns = [
    path('admin/user-management/', views.user_management, name='user_management'),
    path('admin/verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('403/', views.permission_denied_view, name='permission_denied'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/', views.profile, name='profile'),

    # # URL‌های بازیابی رمز عبور
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('members/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'),name='password_reset_done'),
    # path('members/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='members/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('members/reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'),name='password_reset_complete'),

# URL‌های بازیابی رمز عبور
#     path('password_reset/',
#          auth_views.PasswordResetView.as_view(
#              template_name='members/password_reset.html',
#              email_template_name='members/password_reset_email.html',
#              subject_template_name='members/password_reset_subject.txt'
#          ),
#          name='password_reset'),
#     path('password_reset/done/',
#          auth_views.PasswordResetDoneView.as_view(
#              template_name='members/password_reset_done.html'
#          ),
#          name='password_reset_done'),
#     path('reset/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='members/password_reset_confirm.html'
#          ),
#          name='password_reset_confirm'),
#     path('reset/done/',
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='members/password_reset_complete.html'
#          ),
#          name='password_reset_complete'),
]