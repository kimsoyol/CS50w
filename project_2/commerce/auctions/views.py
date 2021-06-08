from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView

from .models import User, Listing, WatchList


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all
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


def item(request, item_id):
    if request.method == "POST":
        f = WatchList.objects.create(author_id=request.user.id, item_id=item_id)
        
        f.save()
        return HttpResponseRedirect(reverse("item", args=[item_id]),{
            "message": "Successfully add to your Watchlist."
        })
    else:
        item = Listing.objects.get(id=item_id)
        try:
            watchitem = WatchList.objects.get(item_id=item.id, author_id=request.user.id)
        except WatchList.DoesNotExist:
            return render(request, "auctions/item.html",{
                "item": item,
            })
        else:
            

            return render(request, "auctions/item.html",{
                    "item": item,
                    "watchitem": watchitem
                })


class Create(CreateView):
        model = Listing
        fields = ( "item", "price", "description", "category", "image")
        template_name = "auctions/create.html"

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
        

def watchlist(request):
    items = WatchList.objects.filter(author=request.user.id)
    
    return render(request, "auctions/watchlist.html",{
        "items":items,
    })
    
def removeWatchList(request, item_id):
    if request.method == "POST":
        f = WatchList.objects.get(item_id=item_id, author_id=request.user.id)
        f.delete()
        return HttpResponseRedirect(reverse("index"))
    