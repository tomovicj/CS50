from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse

import json

from .models import *

from .helper import get_client_ip, generate_id, is_valid_email, is_valid_id


def authorize(request):
    type = request.POST.get("type")
    email = request.POST.get("email")
    password = request.POST.get("password")
    next = request.POST.get("next")
    if request.user.is_authenticated:
        if request.method == "POST":
            if type == "logout":
                logout(request)
        return HttpResponseRedirect(reverse("index"))
    if request.method != "POST":
        return render(request, "redirect/authorize.html")
    # POST
    if email == "" or password == "":
        messages.error(request, "All fields are required")
        return HttpResponseRedirect(reverse("authorize"))
    if not is_valid_email(email):
        messages.error(request, "Looks like you entered the invalid email address")
        return HttpResponseRedirect(reverse("authorize"))
    user = User.objects.filter(email=email).first()
    if type == "login":
        if user is None:
            messages.error(request, "Invalid email and/or password")
            return HttpResponseRedirect(reverse("authorize"))
        auth_user = authenticate(request, username=user.get_username(), password=password)
        if auth_user is None:
            messages.error(request, "Invalid email and/or password")
            return HttpResponseRedirect(reverse("authorize"))
        login(request, auth_user)
        if next:
            return HttpResponseRedirect(next)    
        return HttpResponseRedirect(reverse("index"))
    if type == "register":
        confirmation = request.POST.get("password_confirm")
        username = request.POST.get("username")
        if email == "" or username == "" or password == "" or confirmation == "":
            messages.error(request, "All fields are required")
            return HttpResponseRedirect(reverse("authorize"))
        if password != confirmation:
            messages.error(request, "Reentered password doesn't match the password")
            return HttpResponseRedirect(reverse("authorize"))
        if user is not None:
            messages.error(request, "Email already in use")
            return HttpResponseRedirect(reverse("authorize"))
        if User.objects.filter(username=username).first() is not None:
            messages.error(request, "Username already in use")
            return HttpResponseRedirect(reverse("authorize"))
        new_user = User.objects.create_user(username, email, password)
        login(request, new_user)
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse("index"))


def redirect(request, redirect_id):
    redirect_obj = Redirect.objects.filter(id = redirect_id).first()
    if redirect_obj: 
        if request.method == "GET":
            return render(request, "redirect/redirect.html", {
                "redirect_id": redirect_id,
                "redirect_title": redirect_obj.title,
                "redirect_to": redirect_obj.url
            })
        
        if request.method == "POST":
            body = json.loads(request.body)
            ip = get_client_ip(request)
            user_agent = body["user_agent"]
            screen_resolution = body["screen_resolution"]
            language = body["language"]
            fonts = body["font"]
            data = Data(redirect_id = redirect_id ,ip = ip, user_agent=user_agent, screen_resolution=screen_resolution, language=language, fonts=fonts)
            data.save()
            return HttpResponse(status=200)
    return HttpResponse(status=404)


def index(request):
    if not request.user.is_authenticated:
        return render(request, "redirect/index.html")
    
    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")
        id = request.POST.get("custom_id")
        if title == "" or url == "":
            messages.error(request, "Title and Url fields are required", extra_tags="alert-danger")
            return HttpResponseRedirect(reverse("index"))
        if id is not None:
            if not request.user.has_perm("redirect.create_redirect_with_custom_id"):
                messages.error(request, "Only Premium users can create redirects with custom IDs", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("index"))
            if not is_valid_id(id):
                messages.error(request, "Looks like you entered an invalid ID. ID must be 3-15 alphanumeric characters. No spaces or special characters", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("index"))
            if Redirect.objects.filter(id=id).first() is not None:
                messages.error(request, "Unfortunately, that ID is not available", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("index"))
        else:
            while True:
                id = generate_id()
                if Redirect.objects.filter(id = id).first() is None:
                    break
        try:
            redirect = Redirect(id=id, title=title, url=url, author_id=request.user.id)
            redirect.save()
        except:
            messages.error(request, "Looks like an error occurred while creating the redirect", extra_tags="alert-danger")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.success(request, "Redirect successfully created!", extra_tags="alert-success")
            return HttpResponseRedirect(reverse("index"))

    redirects = list(Redirect.objects.filter(author_id = request.user.id).values())
    paginator = Paginator(redirects, 10)
    page_number = request.GET.get('page')
    page_redirects = paginator.get_page(page_number)
    for redirect in page_redirects:
        redirect["data"] = list(Data.objects.filter(redirect_id = redirect["id"]).values())
    return render(request, "redirect/dashboard.html", {"redirects": page_redirects})


@login_required
def profile(request):        
    if request.method == "POST":
        user = request.user
        type = request.POST["type"]
        givenInput = request.POST["new"]
        if givenInput == "":
            messages.error(request, "Field is required", extra_tags="alert-danger")
            return HttpResponseRedirect(reverse("profile"))
        if type == "username":
            if givenInput == user.username:
                messages.error(request, "You cannot set the new username to be exactly the same as the current one", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            try:
                user.username = givenInput
                user.save()
            except:
                messages.error(request, "Looks like an error occurred while changing the username", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            else:
                messages.success(request, "Successfully changed username!", extra_tags="alert-success")
                return HttpResponseRedirect(reverse("profile"))
        if type == "email":
            if not is_valid_email(givenInput):
                messages.error(request, "Looks like you entered the invalid email address", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            if givenInput == user.email:
                messages.error(request, "You cannot set the new email to be exactly the same as the current one", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            try:
                user.email = givenInput
                user.save()
            except:
                messages.error(request, "Looks like an error occurred while changing the email address", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            else:
                messages.success(request, "Successfully changed email address!", extra_tags="alert-success")
                return HttpResponseRedirect(reverse("profile"))
        if type == "password":
            curPass = request.POST["cur_password"]
            if curPass == givenInput:
                messages.error(request, "You cannot set the new password to the given current password", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            if not user.check_password(curPass):
                messages.error(request, "Looks like you entered the wrong current password", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            try:
                user.set_password(givenInput)
                user.save()
            except:
                messages.error(request, "Looks like an error occurred while changing the password", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("profile"))
            else:
                login(request, user)
                messages.success(request, "Successfully changed password!", extra_tags="alert-success")
                return HttpResponseRedirect(reverse("profile"))

    return render(request, "redirect/profile.html")


PREMIUM_GROUP = Group.objects.get(name="Premium Users")
@login_required
def premium(request):
    if request.method == "POST":
        request.user.groups.add(PREMIUM_GROUP)
        messages.success(request, "You successfully become premium user!", extra_tags = "alert-success")
    return HttpResponseRedirect(reverse("profile"))
