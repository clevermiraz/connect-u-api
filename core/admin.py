from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['name', 'username', 'email', 'emailVerified', 'provider', 'providerAccountId', 'is_staff']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('name', 'username', 'email', 'password', 'first_name', 'last_name', 'image', 'emailVerified', 'provider', 'providerAccountId'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
