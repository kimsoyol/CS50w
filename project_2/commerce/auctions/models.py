from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    pass


class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField( upload_to='images/', height_field=None, width_field=None, max_length=None)
    description = models.TextField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("item", kwargs={"item_id": self.pk})

    def __str__(self):
        return f"{self.item}" 
    
    
class WatchList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} {self.item}(id:{self.item_id})"
    

class Bids(models.Model):
    pass


class Comment(models.Model):
    pass