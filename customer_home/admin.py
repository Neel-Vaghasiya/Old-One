from django.contrib import admin
from .models import ReceivedProduct, Cart, cart_detail, Order, Order_Details 
# Register your models here.

admin.site.register(ReceivedProduct)
admin.site.register(Cart)
admin.site.register(cart_detail)
admin.site.register(Order)
admin.site.register(Order_Details)
