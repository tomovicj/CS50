# Generated by Django 4.1.5 on 2023-01-06 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings_comments_bids'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]
