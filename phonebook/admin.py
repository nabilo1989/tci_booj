# from django.contrib import admin
# from .models import Contact
#
# #
# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'mobile', 'phone', 'workplace', 'position')
#     list_filter = ('position', 'workplace')
#     search_fields = ('first_name', 'last_name', 'mobile', 'phone')
#
#     # اضافه کردن متد save_model
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # فقط برای ایجاد رکورد جدید
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import Contact, ContactGroup  # مطمئن شوید این import درست است

admin.site.register(Contact)
admin.site.register(ContactGroup)