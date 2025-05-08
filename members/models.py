from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = [
            ("can_manage_contacts", "Can create, update and delete contacts"),
        ]
    # رفع مشکل تداخل related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        #related_name="customer_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        #related_name="customer_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username