from django.contrib import admin
from dennisapp.models import Customer, Product, Status, Tag
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Status)
admin.site.register(Tag)
