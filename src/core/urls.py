from django.urls import path, include
from rest_framework import routers

from core import views as core_views

urlpatterns = [
    path('signup', core_views.UserCreateView.as_view(), name='signup'),
    path('login', core_views.UserLoginView.as_view(), name='login'),
    path('profile', core_views.RetrieveUpdateUser.as_view(), name='update-retrieve-destroy-user'),
    path('update_password', core_views.UpdatePasswordAPIView.as_view(), name='update-password')
]
