from django.contrib import admin

from .models import Auction_listing, User, Comment, Bid, Watchlist



# Register your models here.
admin.site.register(Auction_listing)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
