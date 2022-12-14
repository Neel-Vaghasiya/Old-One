# Generated by Django 3.2.9 on 2022-07-11 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_home', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.registration')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField()),
                ('shipping_address', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.registration')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='ReceivedProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1200)),
                ('price', models.FloatField()),
                ('images', models.ImageField(upload_to='pics/')),
                ('seller_name', models.CharField(max_length=100)),
                ('seller_email', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'receivedproduct',
            },
        ),
        migrations.CreateModel(
            name='Order_Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_home.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_home.product_details')),
            ],
            options={
                'db_table': 'order_details',
            },
        ),
        migrations.CreateModel(
            name='cart_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_home.cart')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_home.product_details')),
            ],
            options={
                'db_table': 'Cart_details',
            },
        ),
    ]
