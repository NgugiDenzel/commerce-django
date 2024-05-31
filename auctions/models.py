from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    def __str__(self):
        return self.username


class Auction_listings(models.Model):
   # id = models.IntegerField(primary_key=True, default=1, )
    Title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=100)
    is_on_watchlist = models.BooleanField(default=False)
    image = models.ImageField(upload_to='auctions/', default="img")

    def __str__(self):
        return f"{self.Title}"

    def get_highest_bid(self):
        highest_bid = Bid.objects.filter(
            listing=self).order_by('-amount').first()
        return highest_bid


class Comments(models.Model):
    listing = models.ForeignKey(
        Auction_listings, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.user


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField('Auction_listings')

    def __str__(self):
        return self.user.username + "' Watchlist"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid by {self.user.username} on {self.listing.Title}'

    def get_highest_bid(self):
        highest_bid = Bid.objects.filter(
            listing=self).order_by('-amount').first()
        return highest_bid
