from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
        path('customer_home_index', views.customer_home_index, name='customer_home'),
        path('sellProduct',views.sellProduct, name='sellproduct'),
        path('payment', views.payment, name='payment'),
        path('buy', views.buy, name='buy'),
        path('cart/<slug:slug>', views.cart, name='cart'),
        path('search', views.search, name='search'),
        path('read_more/<slug:slug>',views.read_more,name='read_more'),
        path('showCart', views.showCart, name='showCart'),
        path('remove_from_cart/<slug:slug>', views.remove_from_cart, name='remove_from_cart'),
        path('place_order',views.place_order,name="place_order"),
        path('viewOrderhistory', views.ViewOrderHistory, name="viewOrderhistory"),
        path('viewOrderDetailsHistory/<slug:slug>', views.ViewOrderHistoryDetails, name="viewOrderHistoryDetails"),
]