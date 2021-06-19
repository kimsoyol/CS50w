from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.db.models import Max
from django import forms

from .models import User, Listing, WatchList, Comment, Bid, Category


class commentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'style': "width: 300px; height: 100px; right: 150px",
               'placeholder': 'Your message'}
    )
    )

    class Meta:
        model = Comment
        fields = ['text']


class bidForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Place your bid'}
    ))

    class Meta:
        model = Comment
        fields = ['amount']


def index(request):
    items =  Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "items": items
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


@login_required
def item(request, item_id):
    # adding to WatchList
    if request.method == "POST":
        WatchList.objects.create(author_id=request.user.id, item_id=item_id)
        messages.success(request, "Successfully add to your Watchlist.")
        return HttpResponseRedirect(reverse("item", args=[item_id]))
    else:

        # getting specific item
        item = Listing.objects.get(id=item_id)
        author = str(item.author)
        # getting the Highest bid amount of an item
        if item.bidItem.all():
            highest = float(item.bidItem.filter(
                item_id=item_id).aggregate(Max('amount'))['amount__max'])
            # getting the Highest Bidder
            f = item.bidItem.get(amount=highest)
            highestBidder = str(f.author)
        else:
            highest = 0
            highestBidder = ''

        if not item.active:
            print("item is not active")

            print("Highest bidder and user is same")

        if author == request.user.username:
            print("author and user is same")

        if item.active and (highestBidder == request.user.username or author == request.user.username):

            if highestBidder == request.user.username and not item.active:
                messages.success(request, "You have won the bid.")
            # Handling for an item is in Watchlist or not
            try:
                watchitem = WatchList.objects.get(
                    item_id=item.id, author_id=request.user.id)
            except WatchList.DoesNotExist:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "form": commentForm,
                    "bidsform": bidForm,
                    "highest": highest,
                    "highestBidder": highestBidder,
                    'author': author
                })
            else:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "watchitem": watchitem,
                    "form": commentForm,
                    "bidsform": bidForm,
                    "highest": highest,
                    "highestBidder": highestBidder,
                    'author': author,

                })

        else:
            messages.info(request, "The item is no longer available.")
            return HttpResponseRedirect(reverse('index'))


@login_required
def removeListing(request, item_id):
    if request.method == 'POST':
        f = Listing.objects.get(item_id=item_id, author_id=request.user.id)
        f.active = False
    return HttpResponseRedirect(reverse('item', args=[item_id]))



class Create(CreateView):
    model = Listing
    fields = ("item", "price", "description", "categories", "image" )
    template_name = "auctions/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def watchlist(request):
    items = WatchList.objects.filter(author=request.user.id)

    return render(request, "auctions/watchlist.html", {
        "items": items,
    })


@login_required
def removeWatchList(request, item_id):
    if request.method == "POST":
        f = WatchList.objects.get(item_id=item_id, author_id=request.user.id)
        f.delete()
        return HttpResponseRedirect(reverse("index"))

@login_required
def comment(request, item_id):
    if request.method == 'POST':

        # getting comment and save
        form = commentForm(request.POST)
        if form.is_valid():
            com = form.cleaned_data["text"]
            Comment.objects.create(
                text=com, post_id=item_id, author_id=request.user.id)
        return HttpResponseRedirect(reverse("item", args=[item_id]))


@login_required
def bid(request, item_id):
    if request.method == 'POST':

        # getting user bid
        form = bidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

            # getting starting price
            item = Listing.objects.get(id=item_id)
            price = float(item.price)

            # getting highest bid
            highest = Bid.objects.filter(item_id=item_id).aggregate(
                Max('amount'))['amount__max']

            # comparing bids and save the highest bid
            if not highest and float(amount) > price:
                Bid.objects.update_or_create(
                    amount=amount, item_id=item_id, author_id=request.user.id)
                messages.success(request, "Your bid was added.")
                return HttpResponseRedirect(reverse("item", args=[item_id]))
            elif highest and float(amount) > float(highest):
                Bid.objects.update_or_create(
                    amount=amount, item_id=item_id, author_id=request.user.id)
                messages.success(request, "Your bid was added.")
                return HttpResponseRedirect(reverse("item", args=[item_id]))
            else:
                messages.warning(
                    request, "Your bid must be higher than current bid.")
                return HttpResponseRedirect(reverse("item", args=[item_id]))

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html",{
        'categories': categories,
    })


def categoryItems(request, category_id ):
    items = Listing.objects.filter(active=True, categories=category_id)
    return render(request, 'auctions/index.html', {
        "items":items,
    })
