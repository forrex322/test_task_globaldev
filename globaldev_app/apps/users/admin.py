from django.contrib import admin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
