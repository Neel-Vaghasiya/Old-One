# Generated by Django 3.2.9 on 2022-07-11 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('email', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('role', models.CharField(max_length=50)),
                ('otp', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]