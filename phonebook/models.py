from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام گروه")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "گروه مخاطبین"
        verbose_name_plural = "گروه‌های مخاطبین"
class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    mobile = models.CharField(max_length=11, verbose_name='تلفن همراه')
    phone = models.CharField(max_length=11, blank=True, verbose_name='تلفن ثابت')
    workplace = models.CharField(max_length=100, blank=True, verbose_name='محل کار')
    position = models.CharField(max_length=100, blank=True, verbose_name='سمت شغلی')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        null=True,  # اضافه کردن این خط
        blank=True,  # اضافه کردن این خط
        verbose_name='ایجاد کننده'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"