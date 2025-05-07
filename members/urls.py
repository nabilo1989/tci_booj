from django.urls import path
from . import views
app_name = 'members'  # این خط مهم است - تعریف namespace
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]