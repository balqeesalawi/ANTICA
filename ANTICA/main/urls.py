from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='users-profile'),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('auctions/', views.auctions_index, name='index'),
    path('auctions/<int:pk>', views.AuctionDetail.as_view(), name='auctions_detail'),
    path('auctions/create/', views.AuctionCreate.as_view(), name='auctions_create'),

    path('accounts/signup/', views.signup, name='signup')
]

