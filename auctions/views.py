from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Auction_listing, Comment, Bid, Watchlist
from django.core.exceptions import ValidationError
from django.contrib import messages



class CreateListing(forms.Form):
    title = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title','class': 'form-control','style':'width:600px; margin:10px;'}))
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control','style':'width:600px; margin:10px;'}))
    starting_bid = forms.IntegerField(min_value=0, label='', widget=forms.NumberInput(attrs={'placeholder': 'Starting Bid','class': 'form-control','style':'width:600px; margin:10px;'}))
    img_url = forms.URLField(label='', required=False,widget=forms.URLInput(attrs={'placeholder': 'Image URL (Optional)','class': 'form-control','style':'width:600px; margin:10px;'}))
    choices = Auction_listing.CATEGORY_CHOICES
    category = forms.ChoiceField(label='', choices=choices, required=False, widget=forms.Select(attrs={'placeholder': 'Category (Optional)','class': 'form-control','style':'width:600px; margin:10px;'}))

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Comment','class': 'form-control','style':'width:600px;'}))

class BidForm(forms.Form):
    bid = forms.IntegerField(min_value=0, label='', widget=forms.NumberInput(attrs={'placeholder': 'Bid','class': 'form-control','style':'width:600px;'}))


def index(request):
    lists = Auction_listing.objects.filter(status=True)
    return render(request, "auctions/index.html",{
        "lists" : lists
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

@login_required
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


@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            new_list = Auction_listing(title=title, description=description, price=price, image_url=image_url, category=category, creator=request.user)
            new_list.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html",{
                "form" : form

             })
      


    return render(request, "auctions/create.html",{
        "form" : CreateListing()

    })

def listing(request, listing_id):
    
    listing = Auction_listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    watched = False
    try:
        if Watchlist.objects.filter(listing=listing).filter(user=request.user):
            watched = True
        else:
            watched = False
    except TypeError:
        watched = False
  
    
    return render(request, "auctions/listing.html",{
       "listing": listing,
       "comment": CommentForm(),
       "comments":comments,
       "bid_form": BidForm(),
       "watched": watched    
    })

def categories(request):
    lists = []
    categories = Auction_listing.CATEGORY_CHOICES
    for category in categories:
        lists.append(category[1])
    return render(request, "auctions/categories.html",{
       "categories": lists,
    })

def category(request, category):
    for category_choice in Auction_listing.CATEGORY_CHOICES:
        if category_choice[1] == category:
            category_value = category_choice[0]

    lists = Auction_listing.objects.filter(category=category_value)
    return render(request, "auctions/category.html",{
       "lists": lists,
       "category": category
    })


def comment(request, listing_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data["comment"]
        user = request.user
        listing = Auction_listing.objects.get(pk=listing_id)
        comment = Comment(content=content, user=user, listing=listing)
        comment.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))

def bid(request, listing_id):    
    form = BidForm(request.POST)
    if form.is_valid():
        bid = form.cleaned_data["bid"]
        user = request.user
        listing = Auction_listing.objects.get(pk=listing_id)

        if Bid.objects.filter(listing=listing):
            high_bid = 0     
            for bid1 in Bid.objects.filter(listing=listing):
                if bid1.bid > high_bid:
                    high_bid = bid1.bid 
            if bid > high_bid:
                new_bid = Bid(bid=bid, user=user, listing=listing)
                new_bid.save()
                listing.price = bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))
            else:
                messages.error(request, message="please bid for a higher value.")
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))         
        else:
            if bid >= listing.price:
                new_bid = Bid(bid=bid, user=user, listing=listing)
                new_bid.save()
                listing.price = bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))
            else:
                messages.error(request, message="please bid for a higher value.")
                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))         
    else:
        messages.error(request, message="form value is not valid.")
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))

def watch(request, listing_id):
    listing = Auction_listing.objects.get(pk=listing_id)
    wl = Watchlist(listing=listing, user=request.user)
    wl.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))

def unwatch(request, listing_id):
    listing = Auction_listing.objects.get(pk=listing_id)
    Watchlist.objects.filter(listing=listing).filter(user=request.user).delete()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))

def watchlist(request):
    lists = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html",{
       "lists": lists
    })

def close(request, listing_id):
    listing = Auction_listing.objects.get(pk=listing_id)
    listing.status = False
    listing.save()

    if Bid.objects.filter(listing=listing):
        high_bid = 0     
        for bid in Bid.objects.filter(listing=listing):
            if bid.bid > high_bid:
                high_bid = bid.bid 

        bid = Bid.objects.filter(listing=listing).get(bid=high_bid)
        listing.winner = bid.user
        listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))
