from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import util

import markdown2
import random


def index(request):
    entries = util.list_entries()

    try:
        q = request.GET["q"]
    except:
        q = None

    if not q:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

    if q in entries:
        return redirect(f"wiki/{q}")

    list = []
    for entry in entries:
        if q in entry:
            list.append(entry)

    if list:        
        return render(request, "encyclopedia/index.html", {
                "entries": list
            })
    return render(request, "encyclopedia/error.html", {
        "text": "Sorry, but entry you entered dose not exist."
    })

def entry(request, title):
    text = util.get_entry(title)
    if text:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "text": markdown2.markdown(text)
        })
    
    return render(request, "encyclopedia/error.html", {
            "text": "Sorry, but entry you entered dose not exist."
        })

def random_entry(request):
    entries = util.list_entries()
    return redirect(f"wiki/{random.choice(entries)}")

def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        text =  request.POST["text"]
        if title and text:
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "text": "Encyclopedia entry already exists with the provided title."
                })
            
            util.save_entry(title, text)
            return redirect(f"wiki/{title}")
        
        return render(request, "encyclopedia/error.html", {
            "text": "Both fields are required."
        })

    return render(request, "encyclopedia/add.html")

def edit(request, title):
    if request.method == "POST":
        text = request.POST["text"]
        if text:
            util.save_entry(title, text)
            return redirect(f"/wiki/{title}")

        return render(request, "encyclopedia/error.html", {
            "text": "That field is required."
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "text": util.get_entry(title)
    })