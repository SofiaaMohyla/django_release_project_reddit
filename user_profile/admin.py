from django.contrib import admin

from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', )
    list_display_links = ('id', 'image', )
    readonly_fields = ['admin_panel_image']

admin.site.register(Profile, ProfileAdmin)