from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='users-profile'),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('auctions/', views.auctions_index, name='index'),
    path('auctions/<int:auction_id>', views.auctions_detail, name='auctions_detail'),
    path('auctions/create/', views.AuctionCreate.as_view(), name='auctions_create'),
    path('auctions/<int:pk>/update/', views.AuctionUpdate.as_view(), name='auctions_update'),
    path('auctions/<int:pk>/', views.AuctionDelete.as_view(), name='auctions_delete'),

    path('auctions/<int:auction_id>/add_bid', views.add_bid, name='bids_create'),

    path('accounts/signup/', views.signup, name='signup')
]

