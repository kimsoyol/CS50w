from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.db.models import Max

from .models import User, Listing, WatchList, Comment, Bid

from django import forms

class commentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'style': "width: 300px; height: 100px; right: 150px", 'placeholder': 'Your message'}
        ))

    class Meta:
        model = Comment
        fields = ['text']

class bidForm(forms.ModelForm):
    amount = forms.DecimalField()

    class Meta:
        model = Comment
        fields = ['amount']

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
        # getting the Highest bid amount
        highest = float(item.bidItem.filter(item_id=item_id).aggregate(Max('amount'))['amount__max'])
        # getting the Highest Bidder
        highestBidder = item.bidItem.get(amount=highest)
        try:
            watchitem = WatchList.objects.get(item_id=item.id, author_id=request.user.id)
        except WatchList.DoesNotExist:
            return render(request, "auctions/item.html",{
                "item": item,
                "form": commentForm,
                "bidsform": bidForm,
                "highest": highest,
                "highestBidder": highestBidder.author
            })
        else:
            return render(request, "auctions/item.html",{
                    "item": item,
                    "watchitem": watchitem,
                    "form": commentForm,
                    "bidsform": bidForm,
                    "highest": highest,
                    "highestBidder": highestBidder.author
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


def comment(request, item_id):
    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            com = form.cleaned_data["text"]
            f = Comment.objects.create(text=com, post_id=item_id, author_id=request.user.id)
            f.save()
        return HttpResponseRedirect(reverse("item", args=[item_id]))


def bid(request, item_id):
    if reques.method == 'POST':
        form = bidForm(request.POST)
        if form.is_valid():
            amount = form.cleared_data["amount"]
            f = Bid.objects.create(amount=amount, item_id=item_id, author=request.user.id)
            f.save()
        return HttpResponseRedirect(reverse("item", args=[item_id]))