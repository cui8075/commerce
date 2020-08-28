# Generated by Django 3.1 on 2020-08-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200824_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='category',
            field=models.CharField(blank=True, choices=[('FA', 'Fashion'), ('TO', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), (None, 'No category listed')], default=None, max_length=2, null=True),
        ),
    ]