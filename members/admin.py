# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, Contact, ContactGroup
# from django.contrib.admin import AdminSite
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin')
#     list_filter = ('is_admin', 'is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
#         }),
#     )
#     search_fields = ('email', 'username')
#     ordering = ('username',)
#
# admin.site.register(CustomUser, CustomUserAdmin)
# # در admin.py
#
#
# class CustomAdminSite(AdminSite):
#     site_header = 'مدیریت دفترچه تلفن'
#     site_title = 'پنل مدیریت'
#     index_title = 'خوش آمدید'
#
# custom_admin_site = CustomAdminSite(name='custom_admin')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Contact, ContactGroup

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_verified')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(ContactGroup)