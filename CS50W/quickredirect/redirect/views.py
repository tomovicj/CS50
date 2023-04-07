from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.urls import reverse

import json

from .models import *

from .helper import get_client_ip, generate_id


def authorize(request):
    if not request.user.is_authenticated:
        if request.method == "GET":  
            return render(request, "redirect/authorize.html")

        if request.method == "POST":
            type = request.POST["type"]
            email = request.POST["email"]
            password = request.POST["password"]
            if type == "login":
                try:
                    username = User.objects.filter(email=email).first().username
                except:
                    return render(request, "redirect/authorize.html", {"message": "Looks like that email is not registered yet"})
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "redirect/authorize.html", {"message": "Invalid email and/or password."})

            if type == "register":
                confirmation = request.POST["password_confirm"]
                username = request.POST["username"]
                if password != confirmation:
                    return render(request, "redirect/authorize.html", {"message": "Passwords must match."})
                already_email = User.objects.filter(email=email).first()
                already_username = User.objects.filter(username=username).first()
                if already_email:
                    return render(request, "redirect/authorize.html", {"message": "Email is taken."})
                if already_username:
                    return render(request, "redirect/authorize.html", {"message": "Username is taken."})
                
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        if request.method == "POST":
            type = request.POST["type"]
            if type == "logout":
                logout(request)
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

    return HttpResponseRedirect(reverse("index"))


def index(request):
    if not request.user.is_authenticated:
        return render(request, "redirect/index.html")
    message = {}
    if request.method == "POST":
        title = request.POST["title"]
        url = request.POST["url"]
        if title == "" or url == "":
            message["type"] = "danger"
            message["text"] = "Title and Url fields are required!"
        if not message:
            while True:
                id = generate_id()
                if Redirect.objects.filter(id = id).first() is None:
                    break
            try:
                redirect = Redirect(id=id, title=title, url=url, author_id=request.user.id)
                redirect.save()
            except:
                message["type"] = "danger"
                message["text"] = "Looks like error occurred"
            else:
                message["type"] = "success"
                message["text"] = "Successfully created!"
    
    redirects = list(Redirect.objects.filter(author_id = request.user.id).values())
    paginator = Paginator(redirects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for redirect in page_obj:
        redirect["data"] = list(Data.objects.filter(redirect_id = redirect["id"]).values())
    return render(request, "redirect/dashboard.html", {"redirects": page_obj, "message": message})


def profile(request):
    message = {}
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authorize"))
    if request.method == "POST":
        type = request.POST["type"]
        givenInput = request.POST["new"]
        if givenInput == "":
            return render(request, "redirect/profile.html", {"message": {"type": "danger", "text": "Field is required"}})
        user = request.user
        if type == "username":
            if givenInput != user.username:
                try:
                    user.username = givenInput
                    user.save()
                except: pass
                else:
                    message["type"] = "success"
                    message["text"] = "Successfully changed username!"
        if type == "email":
            if givenInput != user.email:
                try:
                    user.email = givenInput
                    user.save()
                except: pass
                else:
                    message["type"] = "success"
                    message["text"] = "Successfully changed email!"
        if type == "password":
            curPass = request.POST["cur_password"]
            if curPass == givenInput:
                return render(request, "redirect/profile.html", {"message": {"type": "danger", "text": "You can not set the new password to the given current password"}})
            if user.check_password(curPass):
                try:
                    user.set_password(givenInput)
                    user.save()
                except: pass
                else:
                    # Keep user logged in after password change
                    login(request, user)
                    message["type"] = "success"
                    message["text"] = "Successfully changed password!"
            else:
                return render(request, "redirect/profile.html", {"message": {"type": "danger", "text": "Looks like you entered the wrong current password"}})
    return render(request, "redirect/profile.html", {"message": message})


PREMIUM_GROUP = Group.objects.get(name="Premium Users")
def premium(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authorize"))
    if request.method == "POST":
            request.user.groups.add(PREMIUM_GROUP)
    return HttpResponseRedirect(reverse("profile"))
