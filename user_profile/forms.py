from django.forms import ModelForm
from .models import Profile

class ProfileChangeForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image')