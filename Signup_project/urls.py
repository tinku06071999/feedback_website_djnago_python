"""Signup_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("signup", views.signupview, name="signup"),
    path("success", views.signup_success_view, name="signup_success"),
    path("login", views.Login, name="login"),
    path("next", views.Next, name="next"),
    path("suggestion", views.suggestion_submit, name="suggestion_submit"),
    path("suggestion/success/", views.suggestion_success, name="suggestion_success"),
    path("logout", views.logout, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path(
        "forgot-password_succes/",
        views.forgot_password_success,
        name="forgot_password_success",
    ),
    path(
        "reset-password/<str:reset_token>/",
        views.recovery_password,
        name="recovery_password",
    ),
]
