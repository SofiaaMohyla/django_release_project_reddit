from django.urls import path
from .views import CustomLoginView, CustomRegistrationView, logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', CustomRegistrationView.as_view(), name='register')
]
