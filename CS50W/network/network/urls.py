
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create, name="create"),
    path("feed/<str:type>", views.load_feed, name="feed_load"),
    path("like", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
