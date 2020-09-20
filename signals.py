from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from .models import *

def create_customer(sender, created, instance, *args, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name = instance.username,
        )
        print('Customer created')
post_save.connect(create_customer, sender=User)

def update_customer(sender, created, instance, *args, **kwargs):
    if created==False:
        instance.customer.save()
        print('Customer is updated')
post_save.connect(update_customer, sender=User)
