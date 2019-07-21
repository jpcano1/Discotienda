""" Project admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from .models import User, Profile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """ User model Admin """

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'created_at', 'modified_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation')
    list_filter = ('reputation', )

admin.site.register(User, CustomUserAdmin)