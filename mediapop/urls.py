"""
URL configuration for twproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path

from mediapop import views

app_name = "index"
urlpatterns = [
    path("login", views.UserLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
    path("media", views.MediaView.as_view(), name="media"),
    path("media/<int:pk>", views.MediaDetailView.as_view(), name="media_detail"),
    re_path("^$|^/$|^index/$", views.IndexView.as_view(), name="index")
]
