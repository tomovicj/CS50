from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import *


def index(request):
    listings = Listing.objects.all()
    bids = Bid.objects.order_by('-bid')
    finished = Winner.objects.all().values()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": bids,
        "finished": [d['listing_id'] for d in finished]
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def add_listing(request):
    if request.method == "POST":
        if request.POST["title"] and request.POST["start_bid"]:
            listing = Listing(
                title=request.POST["title"],
                description = request.POST["description"],
                image = request.POST["image"],
                start_bid = request.POST["start_bid"],
                category = request.POST["category"],
                owner = request.user)
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))

    return render(request, "auctions/create.html", {
        "categories": Listing._meta.get_field("category").choices
    })
    
def categories_list(request):
    category_list = dict(Listing.categories)
    finished = [d['listing_id'] for d in Winner.objects.all().values()]
    listings =  Listing.objects.all()
    categories = set()
    for listing in listings:
        if not listing.pk in finished:
            categories.add(listing.category)
    return render(request, "auctions/categories.html", {
        "category_list": category_list,
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    bids = Bid.objects.order_by('-bid')
    finished = Winner.objects.all().values()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": bids,
        "category": dict(Listing.categories).get(category),
        "finished": [d['listing_id'] for d in finished]
    })


def listing(request, listing_id):
    return render(request, "auctions/listing.html", {
      "listing": Listing.objects.filter(pk = listing_id).first(),
      "bid": Bid.objects.order_by('-bid').filter(listing_id = listing_id).first(),
      "winner": Winner.objects.filter(listing_id = listing_id).first(),
      "watchlist": bool(Watchlist.objects.filter(listing_id = listing_id, user_id = request.user.id))
    })


def listing_end(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        if request.user.id == Listing.objects.filter(id = listing_id).first().owner_id:
            winner_id = Bid.objects.order_by('-bid').filter(listing_id = listing_id).first()
            if winner_id:
                winner_id = winner_id.bidder.id
            winner = Winner(listing_id = listing_id, winner_id = winner_id)
            winner.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    return HttpResponseRedirect(reverse("index"))


def bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        old_bid = Bid.objects.order_by('-bid').filter(listing_id = request.POST["listing_id"]).first()
        if old_bid:
            old_bid = old_bid.bid
        else:
            old_bid = 0
        start_bid = Listing.objects.filter(pk = listing_id).first().start_bid
        new_bid = float(request.POST["bid"])
        if new_bid > old_bid and new_bid > start_bid:
            bid = Bid(listing_id = listing_id, bid = new_bid, bidder_id=request.user.id)
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
        messages.error(request, "Looks like you entered invalid bid amount")
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        watchlist = Watchlist.objects.filter(user_id = request.user.id, listing_id = listing_id).first()
        if watchlist:
            watchlist.delete()
        else:
            watchlist = Watchlist(user_id = request.user.id, listing_id = listing_id)
            watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    watchlist = Watchlist.objects.filter(user_id = request.user.id)
    listings = Listing.objects.filter(pk__in=[x.listing_id for x in watchlist])
    bids = Bid.objects.order_by('-bid')
    return render(request, "auctions/index.html", {
        "title": "Watchlist",
        "listings": listings,
        "bids": bids,
        "finished": []
    })