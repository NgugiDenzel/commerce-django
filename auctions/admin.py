from django.contrib import admin
from .models import User, Auction_listings, Comments, Watchlist, Bid

admin.site.register(Auction_listings)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Bid)

# Register your models here.
