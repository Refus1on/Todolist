from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


class UserCustomAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    readonly_fields = ['last_login', 'date_joined']


admin.site.register(User, UserCustomAdmin)
