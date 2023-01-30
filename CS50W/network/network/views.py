from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow

import json


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        author = request.user.id
        content = data["content"]
        if content:
            post = Post(author_id=author, content=content)
            try:
                post.save()
            except:
                return HttpResponse(status=400)
    return HttpResponse(status=200)


def load_feed(request, type):
    if type == "all":
        posts = Post.objects.all().order_by('-time').values()
    elif type == "following":
        if request.user.is_authenticated:
            followers_qs = Follow.objects.filter(follower_id = request.user.id)
            followers = [follower.pk for follower in followers_qs]
            posts = Post.objects.filter(author_id__in = followers).order_by('-time').values()
    else:
        load_feed(request, "all")

    posts_list = []
    for post in posts:
        post_qs = Post.objects.filter(pk = post["id"]).first()
        author = post_qs.author.username
        likes = post_qs.likes.all()

        # post.pop("_state")
        # post.pop("author_id")

        post["author"] = author
        post["mine"] = author == request.user.username
        post["likes"] = len(likes)
        post["liked"] = request.user in likes

        posts_list.append(post)
    
    return JsonResponse({"posts": posts_list})


@csrf_exempt
def like(request):
    if request.method == "PUT":
        if request.user.is_authenticated:
            user = request.user
            post_id = json.loads(request.body)["post_id"]
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Invalid post_id"})
            post = Post.objects.filter(pk = post_id).first()
            likes = post.likes.all()
            liked = None
            if user in likes:
                user.like.remove(post)
                liked = False
            else:
                user.like.add(post)
                liked = True

            return JsonResponse({"likes": post.likes.count(), "liked": liked})
        
        return JsonResponse({"error": "You must be loged in to like"})
    return HttpResponseRedirect(reverse("index"))


def edit(request, post_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            new_content = json.loads(request.body)["content"]
            if new_content != "":
                post = Post.objects.filter(pk = post_id).first()
                if post.author == request.user:
                    post.content = new_content
                    post.save()
                    return HttpResponse({"status": "True"})
        return HttpResponse({"status": True})
    return HttpResponseRedirect(reverse("index"))