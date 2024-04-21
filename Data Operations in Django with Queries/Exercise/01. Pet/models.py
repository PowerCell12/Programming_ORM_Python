from django.db import models

# Create your models here.
class Pet(models.Model): ## first task
  name = models.CharField(max_length=40)
  species = models.CharField(max_length=40)

