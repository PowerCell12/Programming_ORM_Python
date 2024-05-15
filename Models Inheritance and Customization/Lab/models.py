from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)


class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)


class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


CHOICES = [
    ('Mammals', 'Mammals'),
    ('Birds', 'Birds'),
    ('Reptiles', 'Reptiles'),
    ('Others', 'Others')
]


class ZooKeeper(Employee):
    specialty = models.CharField(max_length=10, choices=CHOICES)
    managed_animals = models.ManyToManyField(to='Animal')


    def clean(self):
        super().clean()

        if self.specialty not in CHOICES:
            raise ValidationError('Specialty must be a valid choice.')

class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)


class ZooDisplayAnimal(Animal):


    class Meta:
        proxy=True


    def display_info(self):
     string = f"Meet {self.name}! It's {self.species} and it's born {self.birth_date}. It makes a noise like '{self.sound}'!"

     extra_info = ''
     if hasattr(self, 'mammal'):
         extra_info = f" Its fur color is {self.mammal.fur_color}."
     elif hasattr(self, 'bird'):
         extra_info = f" Its wingspan is {self.bird.wing_span} cm."
     elif hasattr(self, 'reptile'):
         extra_info = f" Its scale type is {self.reptile.scale_type}."

     string += extra_info

     return string


    def is_endangered(self):
        if self.species == "Orangutan" or self.species == "Green Turtle" or self.species == "Cross River Gorilla":
          return True
        else:
            return False



