from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='main/static/uploads/', default="")
    bio = models.CharField(max_length=250)
    rating = models.IntegerField()

    def __str__(self):
        return self.user.username


