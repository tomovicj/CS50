from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('profile/authorize', views.authorize, name='authorize'),
    path('profile/premium', views.premium, name='premium'),
    path('<str:redirect_id>', views.redirect, name='redirect')
]
