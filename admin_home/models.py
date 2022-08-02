from django.db import models

# Create your models here.
class Product_Details(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    price=models.FloatField()
    description=models.CharField(max_length=10000)
    category=models.CharField(default="Z",max_length=50)
    product_date=models.DateField(auto_now_add=True)
    available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='pics/')
    class Meta:
        db_table="product_details"