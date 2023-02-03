from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
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
    elif type == "profile":
        id = request.GET.get("id")
        if id:
            posts = Post.objects.filter(author_id = id).order_by('-time').values()
        else:    
            username = request.GET.get("username")
            user = User.objects.filter(username = username).first()
            posts = Post.objects.filter(author_id = user.id).order_by('-time').values()
    else:
        load_feed(request, "all")

    # Paginations
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    number_of_pages = paginator.num_pages
    try:
        # returns the desired page object
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(number_of_pages)


    posts_list = []
    for post in list(page_obj.object_list):
        post_qs = Post.objects.filter(pk = post["id"]).first()
        author = post_qs.author.username
        likes = post_qs.likes.all()

        post["author"] = author
        post["mine"] = author == request.user.username
        post["likes"] = len(likes)
        post["liked"] = request.user in likes

        posts_list.append(post)
    
    return JsonResponse({
        "num_pages": number_of_pages,
        "on_page": page_obj.number,
        "posts": posts_list
    })


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
                    return JsonResponse({"status": "True"})
        return JsonResponse({"status": True})
    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    user = User.objects.filter(username = username).first()
    authenticated = request.user.is_authenticated
    following_status = False
    if authenticated:
        following_status = user in [x.followe for x in request.user.follower.all()]
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "followers_count": len(user.followe.all()),
        "following_count": len(user.follower.all()),
        "following_status": following_status,
        "authenticated": authenticated,
        "mine": user.username == request.user.username
    })


@csrf_exempt
def follow(request):
    if request.method == "PUT" and request.user.is_authenticated:
        follower_id = request.user.id
        followe_id = json.loads(request.body)["user_id"]
        follow = Follow.objects.filter(follower_id = follower_id, followe_id = followe_id)
        if follow:
            follow.delete()
        else:
            follow = Follow(follower_id = follower_id, followe_id = followe_id)
            follow.save()
        return HttpResponse(status = 200)
    return HttpResponseRedirect(reverse("index"))