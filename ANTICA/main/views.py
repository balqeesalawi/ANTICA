from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Auction, Bid, Profile
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import BidForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid Sign Up - Try Again"

    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


@login_required
def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, "users/profile.html", {'profile' : profile})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['image', 'email', 'phone', 'bio']




def auctions_index(request):
    auctions = Auction.objects.all
    return render(request, "auctions/index.html", {"auctions": auctions})

@login_required
def auctions_detail(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction= auction)


    if auction.is_active == False:
        for bid in bids:
         if bid.amount == auction.current_price:
            winner = bid.bidder

            message = f"THE WINNER FOR THIS AUCTION IS { winner }"
            return render(request, 'auctions/detail.html', { 'auction': auction, 'message': message, 'bids' : bids, 'winner': winner})

    return render(request, 'auctions/detail.html', {'auction': auction, 'bids' : bids})



class AuctionCreate(LoginRequiredMixin, CreateView):
    model = Auction
    fields = [
        "name",
        "description",
        'date',
        "starting_price",
        "current_price",
        "image",
        "category",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    


class AuctionUpdate(LoginRequiredMixin, UpdateView):
    model = Auction
    fields = ["is_active"]


class AuctionDelete(LoginRequiredMixin, DeleteView):
    model = Auction
    success_url = "/auctions/"


@login_required
def add_bid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.auction_id = auction_id
            new_bid.bidder = request.user

            error_message = ""
            if new_bid.amount <= auction.current_price:
                error_message = (
                    "The amount of the bid should be higher than the current price"
                )
                context = {
                    "form": form,
                    "error_message": error_message,
                    "auction": auction,
                }
                return render(request, "auctions/detail.html", context)

            if new_bid.amount < auction.current_price + 5:
                error_message = "The can't bid with less than 5 BD "
                context = {
                    "form": form,
                    "error_message": error_message,
                    "auction": auction,
                }
                return render(request, "auctions/detail.html", context)


            auction.current_price = new_bid.amount
            auction.save()
            new_bid.save()
    context = {"form": form, "auction": auction}
    return render(request, "auctions/detail.html", context)


