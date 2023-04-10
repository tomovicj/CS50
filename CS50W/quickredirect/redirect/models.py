from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class Redirect(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)        
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.url})"


class Data(models.Model):
    redirect = models.ForeignKey(Redirect, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    screen_resolution = models.CharField(max_length=9, blank=True)
    language = models.CharField(max_length=7, blank=True)
    fonts = models.CharField(max_length=11, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Data for: {self.redirect.title} ({self.redirect.id})"
