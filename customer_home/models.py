from django.db import models
from home.models import Registration
from admin_home.models import Product_Details
# Create your models here.

class ReceivedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    price = models.FloatField()
    images = models.ImageField(upload_to='pics/')
    seller_name=models.CharField(max_length=100)
    seller_email=models.CharField(max_length=100)
    class Meta:
        db_table = 'receivedproduct'

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Registration,on_delete=models.CASCADE,)
    class Meta:
        db_table = "cart"

class cart_detail(models.Model):
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE,)
    product_id=models.ForeignKey(Product_Details,on_delete=models.CASCADE,)
    class Meta:
        db_table="Cart_details"
        
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Registration, on_delete=models.CASCADE,)
    order_date=models.DateField()
    shipping_address=models.CharField(max_length=500)
    status = models.CharField(max_length=100)
    amount = models.IntegerField()
    class Meta:
        db_table = "orders"

class Order_Details(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product_Details, on_delete=models.CASCADE)
    class Meta:
        db_table = "order_details"
