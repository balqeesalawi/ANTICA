from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.

CATEGORY = (
    ('art', 'Art'),
    ('car', 'Cars'),
    ('jewelry', 'Jewelry'),
    ('book', 'Books & Magazines'),
    ('coin', 'Coins'),
    ('fashion', 'Fashion'),
    ('decoration', 'Decoration'),
    ('machine', 'Machines'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='main/static/uploads/', default="")
    bio = models.TextField(max_length=250)
    rating = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("users-profile", kwargs={"profile_id": self.id})

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=250)
    starting_price = models.DecimalField(max_digits=10, decimal_places=3)
    current_price = models.DecimalField(max_digits=10, decimal_places=3)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='main/static/uploads/', default="")
    date = models.DateTimeField()
    category = models.CharField(max_length=12, choices=CATEGORY, default=CATEGORY[0][0])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("auctions_detail", kwargs={"auction_id": self.id})

    def auction_for_today(self):
        now = timezone.now()
        diff = self.date - now
        return diff.total_seconds() <= 86400 and diff.total_seconds() > 0



class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction.name} for {self.bidder.username}"

    def get_absolute_url(self):
        return reverse("auctions_detail", kwargs={"auction_id": self.auction.id})


