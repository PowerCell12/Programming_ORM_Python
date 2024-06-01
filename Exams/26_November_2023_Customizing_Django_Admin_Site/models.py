from django.core import validators
from django.db import models

# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[validators.MaxValueValidator(2005), validators.MinValueValidator(1900)])
    website = models.URLField(blank=True, null=True) # if error do help_text and not blank and null


CHOICES = [
    ("Technology", "Technology"),
    ("Science", "Science"),
    ("Education", "Education"),
]

class Article(models.Model):
    title = models.CharField(max_length=200, validators=[validators.MinLengthValidator(5)])
    content = models.TextField(validators=[validators.MinLengthValidator(10)])
    category = models.CharField(max_length=10, default="Technology", choices=CHOICES)
    authors  = models.ManyToManyField(to=Author) ## if error do related_name
    published_on = models.DateTimeField(editable=False, auto_now_add=True)


class Review(models.Model):
    content = models.TextField(validators=[validators.MinLengthValidator(10)])
    rating = models.FloatField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    author  = models.ForeignKey(to=Author, on_delete=models.CASCADE) ## same as authors up
    article  = models.ForeignKey(to=Article, on_delete=models.CASCADE) ## same as authors up
    published_on = models.DateTimeField(editable=False, auto_now_add=True)
