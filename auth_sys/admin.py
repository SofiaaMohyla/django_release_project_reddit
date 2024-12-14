from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import NewUser


class NewUserAdmin(UserAdmin):
    model = NewUser
    list_display = ('id', 'username', "email", "is_staff", "is_moderator")
    list_display_links = ('id', 'username')
    list_filter = ('id', 'username', "email", "is_staff", "is_moderator",)
    
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_moderator")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "is_staff",
                "is_moderator"
            )}
        ),
    )
    search_fields = ('id', "username",)
    ordering = ("id",)


admin.site.register(NewUser, NewUserAdmin)
