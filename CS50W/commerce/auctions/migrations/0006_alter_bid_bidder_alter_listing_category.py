# Generated by Django 4.1.5 on 2023-01-08 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_bid_time_bid_bidder_alter_bid_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('collectibles-and-art', 'Collectibles and art'), ('electronics', 'Electronics'), ('entertainment-memorabilia', 'Entertainment memorabilia'), ('fashion', 'Fashion'), ('home-and-garden', 'Home and garden'), ('motors', 'Motors'), ('real-estate', 'Real Estate'), ('sporting-goods', 'Sporting goods'), ('toys-and-hobbies', 'Toys and hobbies'), ('tickets-and-travel', 'Tickets and travel'), ('pet-supplies', 'Pet supplies'), ('specialty-services', 'Specialty services'), ('baby-essentials', 'Baby essentials'), ('other', 'Other')], default='other', max_length=25),
        ),
    ]
