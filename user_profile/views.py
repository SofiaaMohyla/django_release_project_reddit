from typing import Any
from django.http import HttpRequest, HttpResponse
from auth_sys.models import NewUser
import auth_sys.forms as user_form
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, UpdateView
from .models import Profile
from django.urls import reverse_lazy

# Create your views here.


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile/profile-detail.html"
    context_object_name = 'profile'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        type_of_activity = self.kwargs.get('ac', 'none')
        if type_of_activity == 'posts':
            self.template_name = "profile/profile-detail-posts.html"
        elif type_of_activity == 'comments':
            self.template_name = "profile/profile-detail-comments.html"
        elif type_of_activity == 'upvoted':
            self.template_name = "profile/profile-detail-upvoted.html"
        elif type_of_activity == 'downvoted':
            self.template_name = "profile/profile-detail-downvoted.html"
            
        return super().get(request, *args, **kwargs)
