import django
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, null=True) # maybe error
    supplier = models.CharField(max_length=150, null=True) # maybe error
    created_on = models.DateTimeField(auto_now_add=True, editable=False, null=True) # if error here
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)
    barcode = models.IntegerField(null=True) # maybe error