# Generated by Django 3.1 on 2020-08-27 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20200827_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='create',
        ),
        migrations.RemoveField(
            model_name='user',
            name='win',
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_item', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='win_item', to=settings.AUTH_USER_MODEL),
        ),
    ]