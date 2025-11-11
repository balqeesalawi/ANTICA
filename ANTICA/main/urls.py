from django.urls import path
from . import views

urlpatterns = [
    # path('profile/', profile, name='users-profile'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    
]

