# Generated by Django 3.1 on 2020-08-24 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='category',
            field=models.CharField(choices=[('FA', 'Fashion'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), (None, 'No category listed')], default=None, max_length=2),
        ),
    ]
