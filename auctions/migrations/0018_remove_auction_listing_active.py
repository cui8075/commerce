# Generated by Django 3.1 on 2020-08-25 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20200825_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_listing',
            name='active',
        ),
    ]