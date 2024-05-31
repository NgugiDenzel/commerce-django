from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms


from .models import User, Auction_listings, Comments, Watchlist, Bid


class Auction_Listing_form(forms.ModelForm):
    class Meta:
        model = Auction_listings
        fields = ['Title', 'description',
                  'starting_bid', 'category', 'image']


class Comment_form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Comment']


def index(request):
    lists = Auction_listings.objects.all()

    return render(request, "auctions/index.html", {'lists': lists})


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


def auction_listing(request):
    form = Auction_Listing_form()
    if request.method == 'POST':
        form = Auction_Listing_form(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('auction'))
    """if request.method == 'POST':
        form1 = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form1 = UploadForm()"""

    return render(request, "auctions/auctionlisting.html", {"form": form, 'form1': form})


def listing_page(request, Title):
    form = Comment_form()
    if request.method == 'POST':
        comment = Comment_form(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('listings', kwargs={'Title': Title}))

    comments = Comments.objects.all()

    lists = Auction_listings.objects.get(Title=Title)
    if request.method == 'POST':
        listing = get_object_or_404(Auction_listings, Title=Title)
        # list = get_object_or_404(Bid, listing=Title)

        new_bid_amount = float(request.POST.get('bid_amount', 0))
        highest_bid = listing.get_highest_bid()

        if highest_bid is None or new_bid_amount > highest_bid.amount:
            bid = Bid(user=request.user, listing=listing,
                      amount=new_bid_amount)
            bid.save()

            listing.starting_bid = new_bid_amount
            listing.save()
            return HttpResponseRedirect(reverse('listings', kwargs={'Title': Title}))
        if request.method == 'POST':
            listing = get_object_or_404(Auction_listings, Title=Title)

        # Check if the user is authenticated and is the creator of the listing
            if request.user.is_authenticated and request.user == listing.creator:
                highest_bid = listing.get_highest_bid()

                if highest_bid:
                    listing.winner = highest_bid.user
                    listing.save()

                    listing.active = False
                    listing.save()
                    return HttpResponseRedirect(reverse('listings', kwargs={'Title': Title}))
            return render(request, "auctions/listing_page.html", {"lists": lists})

    """listing = get_object_or_404(Auction_listings, Title=Title)

    is_on_watchlist = Title in request.user.profile.watchlist.all()

    is_creator = listing.seller == request.user

    highest_bid = listing.get_highest_bid()

    comments = listing.comments.all()
    context = {
        'listing': listing,
        'is_on_watchlist': is_on_watchlist,
        'is_creator': is_creator,
        'highest_bid': highest_bid,
        'comments': comments,
    }"""

    return render(request, "auctions/listing_page.html", {"lists": lists, "form": form, 'comments': comments})


def category(request):
    category = Auction_listings.objects.all()

    return render(request, "auctions/Categories.html", {"category": category})


def category_list(request, category):
    categories = Auction_listings.objects.get(category=category)
    return render(request, "auctions/category_list.html", {"categories": categories})


"""def watchlist(request):
    return render(request, "auctions/watchlist.html")



def add_to_watchlist(request, Title):
    listing = Auction_listings.objects.get(Title=Title)
    watchlist = request.session.get('watchlist', [])

    if Title not in watchlist:
        watchlist.append(Title)
        request.session['watchlist'] = watchlist

    return render(request, 'auctions/watchlist.html', {"Title": Title})


def remove_from_watchlist(request, Title):
    listing = Auction_listings.objects.get(Title=Title)
    watchlist = request.session.get('watchlist', [])

    if Title in watchlist:
        watchlist.remove(Title)
        request.session['watchlist'] = watchlist

    return render(request, 'auctions/watchlist.html', {"Title": Title})

"""


def watchlist(request):
    user_watchlist, created = Watchlist.objects.get_or_create(
        user=request.user)
    listings = user_watchlist.listings.all()
    return render(request, 'auctions/watchlist.html', {'listings': listings})


def add_to_watchlist(request, Title):
    listing = Auction_listings.objects.get(Title=Title)
    user_watchlist, created = Watchlist.objects.get_or_create(
        user=request.user)
    user_watchlist.listings.add(listing)
    listing.is_on_watchlist = True
    listing.save()
    return HttpResponseRedirect(reverse('watchlist'))


def remove_from_watchlist(request, Title):
    listing = get_object_or_404(Auction_listings, Title=Title)
    user_watchlist, created = Watchlist.objects.get_or_create(
        user=request.user)
    user_watchlist.listings.remove(listing)
    listing.is_on_watchlist = False
    listing.save()
    return HttpResponseRedirect(reverse('watchlist'))


# def listing_comments(request, Title):

# def place_bid(request, Title):
