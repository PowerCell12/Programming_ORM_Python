from django.core import validators
from django.db import models

# Create your models here.
class Director(models.Model):
    full_name = models.CharField(max_length=120, validators=[validators.MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')
    years_of_experience = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)])


class Actor(models.Model):
    full_name = models.CharField(max_length=120, validators=[validators.MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

CHOICES  = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Other', 'Other')
]


class Movie(models.Model):
    title = models.CharField(max_length=150, validators=[validators.MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, default='Other', choices=CHOICES)
    rating = models.DecimalField(default=0.0, max_digits=3, decimal_places=1, validators=[validators.MaxValueValidator(10), validators.MinValueValidator(0)]) ## from here
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name='movies')
    starring_actor = models.ForeignKey(to=Actor, blank=True, null=True, on_delete=models.SET_NULL, related_name='movies')
    actors= models.ManyToManyField(to=Actor)