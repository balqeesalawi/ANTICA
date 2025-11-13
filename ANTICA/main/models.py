from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=250)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='main/static/uploads/', default="")
    category = models.CharField(max_length=12, choices=CATEGORY, default=CATEGORY[0][0])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("auctions_detail", kwargs={"pk": self.id})



class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction.name} for {self.bidder.username}"

    def get_absolute_url(self):
        return reverse("auctions_detail", kwargs={"pk": self.auction.id})


