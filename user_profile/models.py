from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to="profile/%Y/%m/%d/", blank=True, null=True)

    def get_image_url(self):
        url = static('img/anonymous_user.png')
        if self.image:
            url = self.image.url
        return url

    def admin_panel_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width=125>')
        
    admin_panel_image.short_description = 'Image'
    admin_panel_image.allow_tags = True

    def __str__(self) -> str:
        return f'{self.user.username}'

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
