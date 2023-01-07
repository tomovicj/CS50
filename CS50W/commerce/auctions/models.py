from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=400)
    start_bid = models.PositiveIntegerField()
    category = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.PositiveIntegerField()
    time = models.DateTimeField()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1000)
