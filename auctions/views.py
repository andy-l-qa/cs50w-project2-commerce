from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES.get("image")
        category = Category.objects.get(name=request.POST["category"])
        price = request.POST["price"]
        seller = request.user

        listing = Listing.objects.create(
            title=title,
            description=description,
            image=image,
            category=category,
            price=float(price),
            seller=seller
        )

        listing.save()
        return HttpResponseRedirect(reverse(index))


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


def display_by_category(request):
    categories = Category.objects.all()

    if request.method == "POST":
        selected_category = request.POST.get("category")

        if selected_category:
            listings = Listing.objects.filter(
                active=True,
                category=selected_category
            )
        else:
            listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
    })


def listing(request, id):
    listing = Listing.objects.get(pk=id)

    in_watchlist = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist
    })