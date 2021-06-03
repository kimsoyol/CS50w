from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    arthur = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField( upload_to='images/', height_field=None, width_field=None, max_length=None)
    description = models.CharField(max_length=50)
    category = models.CharField(max_length=100, blank=True)

class Bids(models.Model):
    pass


class Comment(models.Model):
    pass