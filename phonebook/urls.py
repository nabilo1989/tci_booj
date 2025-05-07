from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('search/', views.search_contacts, name='search_contacts'),
    path('create/', views.contact_create, name='contact_create'),
    path('update/<int:pk>/', views.contact_update, name='contact_update'),
    path('delete/<int:pk>/', views.contact_delete, name='contact_delete'),
]