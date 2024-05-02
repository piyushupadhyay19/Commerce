from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import User, Listing, Category, Bid, Comment
from .forms import ListingForm, BidFrontendForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True).order_by('title')
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username.strip() == "" or email.strip() == "":
            return render(request, "auctions/register.html", {
                "message": "Please fill in all fields."
            })
        elif password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        elif len(password) < 8:
            return render(request, "auctions/register.html", {
                "message": "Password must be at least 8 characters long."
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

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        comments = listing.comments.all()
    except Listing.DoesNotExist:
        return redirect('index')
    if request.method == "POST":
        if "newbid" in request.POST:
            bid_form = BidFrontendForm(request.POST or None, instance=Bid(listing=listing))
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.user = request.user
                bid.listing = listing
                bid.save()
                listing.current_bid = bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "bid_form": bid_form,
                    "comment_form": CommentForm(),
                })
        elif "commentss" in request.POST:
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "bid_form": BidFrontendForm(),
                    "comment_form": comment_form,
                })
        elif "watchlists" in request.POST:
            if request.user in listing.watchlist.all():
                listing.watchlist.remove(request.user)
            else:
                listing.watchlist.add(request.user)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "bid_form": BidFrontendForm(),
            "comment_form": CommentForm(),})

def mylisting(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(user=request.user).order_by('title')
    })

def closedlistings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=False).order_by('title')
    })

def categories(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })

def categorylisting(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category__category=category, active=True).order_by('title'),
        "category": category,
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all().order_by('title')
    })

@login_required(login_url='/login')
def removelisting(request, listing_id):
    try:
        if request.user == Listing.objects.get(pk=listing_id).user:
            listing = Listing.objects.get(id=listing_id)
            listing.delete()
    except Listing.DoesNotExist:
        return redirect('index')

    return redirect('mylistings')

@login_required(login_url='/login')
def closelisting(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.user == Listing.objects.get(pk=listing_id).user and Listing.objects.get(pk=listing_id).active and Listing.objects.get(pk=listing_id).current_bid is not None:
            listing.active = False
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                "comment_form": CommentForm(),
                "error_message": "This listing has no bids yet. If you want to delete it, please choose to remove listing.",})
    except Listing.DoesNotExist:
        return redirect('index')

