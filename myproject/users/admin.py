from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'bio',
                    'job_security_preference', 'expected_income']


admin.site.register(CustomUser, CustomUserAdmin)
