from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.random_entry, name="random"),
    path("add_entry", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit")
]
