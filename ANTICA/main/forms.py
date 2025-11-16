from django import forms
from django.contrib.auth.models import User
from .models import Bid, Profile


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["email", "bio", 'phone', 'image']
