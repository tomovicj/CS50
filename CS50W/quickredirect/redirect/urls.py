from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('profile/authorize', views.authorize, name='authorize'),
    path('<str:redirect_id>', views.redirect, name='redirect')
]
