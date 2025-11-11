from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")

# @login_required
# def profile(request):
#     return render(request, 'users/profile.html')
