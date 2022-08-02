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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
urlpatterns = [
        path('ad/admin_indexPage', views.index, name='index'),
        path('addProduct', views.addProduct, name='addProduct'),
        path('viewProduct', views.viewProduct, name='viewProduct'),
        path('DeleteProduct/<slug:slug>', views.deleteProduct, name='deleteProduct'),
        path('UpdateProduct/<slug:slug>', views.updateProduct, name='updateProduct'),
        path('UpdateProfile', views.updateProfile, name='updateProfile'),
        path('signout', views.signout, name='signout'),
        path('AddAdmin', views.addAdmin, name='addAdmin'),
        path('viewReceivedProduct',views.viewReceivedProduct,name='viewReceivedProduct'),
        path('Accept/<slug:slug>', views.AcceptProduct, name='accept'),
        path('Reject/<slug:slug>',views.RejectProduct, name='reject'),
        path('viewOrder', views.ViewOrder, name="viewOrder"),
        path('viewOrderDetails/<slug:slug>', views.ViewDetails, name="viewOrderDetails"),
        path('makedone/<slug:slug>',views.MakeDone,name="MakeDone"),
        
]

