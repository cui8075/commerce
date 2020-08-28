# Generated by Django 3.1 on 2020-08-26 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20200826_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='win',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auctions.auction_listing'),
        ),
    ]
