"""Ecommerce URL Configuration

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
urlpatterns = [
        path('', views.index, name='index'),
        path('login', views.login, name='login'),
        path('auth', views.auth_view, name='auth'),
        # path('invalidlogin', views.invalidlogin, name='invalidlogin'),
        path('logout', views.logout, name='logout'),
        # path('loggedin', views.loggedin, name='loggedin'),
        path('register', views.register, name='register'),
        path('term_condition', views.term_condition, name='term_condition'),
        path('about_us', views.about_us, name='about_us'),
        path('contact',views.contactUs, name='contactUs'),
        path('forgot',views.forgot, name='forgot'),
        path('otp',views.otp,name='otp'),
        path('check_otp',views.check_otp,name='check_otp'),
        path('verify',views.verify,name='verify'),
]
