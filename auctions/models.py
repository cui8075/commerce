from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    FASHION = 'FA'
    TOYS = 'TO'
    ELECTRONICS = 'EL'
    HOME = 'HO'

    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image_url = models.URLField(blank=True)

    CATEGORY_CHOICES = [
    (FASHION, 'Fashion'),
    (TOYS, 'Toys'),
    (ELECTRONICS, 'Electronics'),
    (HOME, 'Home'),
    ('', 'No category listed (Optional)')
    ]

    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=None,
        blank=True
    )
    status = models.BooleanField(default=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="create_item")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="win_item")
    def __str__(self):
        return f"{ self.id } : {self.title}"
    

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{ self.id } : {self.content}"

class Bid(models.Model):
    bid = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"id number{ self.id } : {self.listing} bid by {self.user} for price ${self.bid} "

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watched_item")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="list")

    def __str__(self):
        return f"{ self.id } : {self.user} {self.listing}"
