# Generated by Django 3.1 on 2020-08-25 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_user_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='create',
        ),
    ]
