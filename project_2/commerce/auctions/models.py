from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}" 
     

class Listing(models.Model):

    categoryChoices = [('Fashion', 'Fashion'), ('Home', 'Home'), ('Electronics', 'Electronics'), ('Toy', 'Toy')]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField( upload_to='images/', height_field=None, width_field=None, max_length=None)
    description = models.TextField(max_length=50, blank=True)
    categories = models.ForeignKey(Category, blank=True , on_delete=models.CASCADE, null=True, related_name='itemCategory')
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("item", kwargs={"item_id": self.pk})

    def __str__(self):
        return f"{self.item}" 
    
    
class WatchList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} {self.item}(id:{self.item_id})"
    


class Comment(models.Model):
    text = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}-{self.author} : {self.text}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bidItem')
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.item}-{self.author} : {self.amount}"