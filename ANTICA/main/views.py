from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Auction
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")

def signup(request):
    error_message =''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Sign Up - Try Again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')

def auctions_index(request):
    auctions = Auction.objects.all
    return render(request, 'auctions/index.html', {'auctions': auctions})

class AuctionDetail(DetailView):
    model = Auction

class AuctionCreate(LoginRequiredMixin,CreateView):
    model = Auction
    fields = ['name', 'description', 'starting_price', 'current_price','image', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
