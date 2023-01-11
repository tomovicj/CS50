from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/end", views.listing_end, name="listing_end"),
    path("create", views.add_listing, name="create"),
    path("categories", views.categories_list, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
]
