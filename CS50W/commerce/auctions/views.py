from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid


def index(request):
    listings = Listing.objects.all()
    bids = Bid.objects.all().order_by("bid")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": 
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


def listing(request, listing_id):
    pass


@login_required()
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

    return render(request, "auctions/create.html")
    
