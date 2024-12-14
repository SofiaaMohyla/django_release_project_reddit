from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import NewUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ("username", )

class NewUserChangeForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ('username', 'email')