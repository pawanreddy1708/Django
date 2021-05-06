from django.db import models
from user.models import User
# Create your models here.

class Products(models.Model):
    brand=models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    image = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.model

class Cart(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
    quantity = models.IntegerField()

class Order(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
    address = models.CharField(max_length=1024)
    phone = models.BigIntegerField()
    total_price = models.FloatField()
    total_items = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

class WishList(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
