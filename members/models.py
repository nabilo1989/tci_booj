from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


    # رفع مشکل تداخل related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='گروه‌ها',
        blank=True,
        help_text='گروه‌هایی که کاربر به آنها تعلق دارد.',
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='مجوزهای کاربر',
        blank=True,
        help_text='مجوزهای خاص این کاربر.',
        related_name="customuser_permissions",
        related_query_name="customuser",
    )



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
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, verbose_name="آدرس")
    groups = models.ManyToManyField(ContactGroup, blank=True, verbose_name="گروه‌ها")
    created_by = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        verbose_name="ایجاد کننده",
        related_name='members_contacts'  # این خط اضافه شد
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "مخاطب"
        verbose_name_plural = "مخاطبین"
        ordering = ['last_name', 'first_name']





class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
        ('O', 'سایر'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="شماره تلفن باید به این فرمت وارد شود: '+999999999'")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name='تلفن همراه')
    national_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد ملی')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='جنسیت')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    bio = models.TextField(blank=True, null=True, verbose_name='درباره من')
    website = models.URLField(blank=True, null=True, verbose_name='وبسایت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"پروفایل {self.user.get_full_name() or self.user.username}"

    def get_age(self):
        if self.birth_date:
            import datetime
            return datetime.date.today().year - self.birth_date.year
        return None


# سیگنال‌ها برای ایجاد خودکار پروفایل هنگام ساخت کاربر
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()