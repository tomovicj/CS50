from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class User(AbstractUser):
    pass


class Listing(models.Model):
    categories = [
        ("collectibles-and-art", "Collectibles and art"),
        ("electronics", "Electronics"),
        ("entertainment-memorabilia", "Entertainment memorabilia"),
        ("fashion", "Fashion"),
        ("home-and-garden", "Home and garden"),
        ("motors", "Motors"),
        ("real-estate", "Real Estate"),
        ("sporting-goods", "Sporting goods"),
        ("toys-and-hobbies", "Toys and hobbies"),
        ("tickets-and-travel", "Tickets and travel"),
        ("pet-supplies", "Pet supplies"),
        ("specialty-services", "Specialty services"),
        ("baby-essentials", "Baby essentials"),
        ("other", "Other")
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=400)
    start_bid = models.FloatField()
    category = models.CharField(max_length=25, choices=categories, default="other")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bidder.username}: ${str('%.2f' % self.bid)}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1000)


class Winner(models.Model):
    winner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        if self.winner:
            return self.winner.username
        return "No one"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.listing.id)