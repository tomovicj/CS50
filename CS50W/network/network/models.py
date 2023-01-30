from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
        like = models.ManyToManyField('network.Post', blank=True, related_name="likes")


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followe = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followe")

    def __str__(self):
        return f"{self.follower} follows {self.followe}"
