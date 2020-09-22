from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, null=True)
    phone = models.CharField(max_length = 200, null=True)
    email = models.CharField(max_length = 200, null=True)
    profile = models.ImageField(null=True,default="sg.png", blank=True)
    date = models.DateTimeField(auto_now_add = True, null=True)
    def __str__(self):
        return str(self.name)



class Tag(models.Model):
    name = models.CharField(max_length = 200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('indoor', 'indoor'),
        ('outdoor', 'outdoor'),
    )
    name = models.CharField(max_length = 200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length = 200, null=True, choices = CATEGORY)
    description = models.CharField(max_length = 200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add = True, null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name

class Status(models.Model):
    STATUS = (
        ('pending','pending'),
        ('delivered','delivered'),
        ('out for delivery', 'out for delivery'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices = STATUS)
    note = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.product.name



