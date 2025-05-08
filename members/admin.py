from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


admin.site.site_header = 'پنل مدیریت دفترچه تلفن'
admin.site.site_title = 'مدیریت سایت'
admin.site.index_title = 'خوش آمدید به پنل مدیریت'
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)