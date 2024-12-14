from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class NewUser(AbstractUser):
    is_moderator = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username