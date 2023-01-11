# Generated by Django 4.1.5 on 2023-01-08 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_listings_id_bid_listing_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='time',
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_bid',
            field=models.FloatField(),
        ),
    ]
