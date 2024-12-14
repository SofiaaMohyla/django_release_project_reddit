from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, ListView
from .forms import MyUserCreationForm
from user_profile.models import Profile
from django.conf import settings
from django.contrib.auth import logout


# Create your views here.

class CustomLoginView(LoginView):
    model = settings.AUTH_USER_MODEL
    template_name = 'auth_sys/login.html'
    redirect_authenticated_user = True
    
class CustomRegistrationView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = MyUserCreationForm
    template_name="auth_sys/register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        Profile.objects.create(user=form.instance).save()
        
        return response

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)