from django.core import validators
from django.db import models
from django.db.models import Count


# Create your models here.


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(count_articles=Count('article__id')).order_by('-count_articles', 'email')



class Author(models.Model):
    full_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(validators=[validators.MaxValueValidator(2005), validators.MinValueValidator(1900)])
    website = models.URLField(blank=True, null=True)
    objects = AuthorManager()

CHOICES = [
    ("Technology", "Technology"),
    ("Science", "Science"),
    ("Education", "Education"),
]

class Article(models.Model):
    title = models.CharField(max_length=200, validators=[validators.MinLengthValidator(5)])
    content = models.TextField(validators=[validators.MinLengthValidator(10)])
    category = models.CharField(max_length=10, default="Technology", choices=CHOICES)
    authors  = models.ManyToManyField(to=Author)
    published_on = models.DateTimeField(editable=False, auto_now_add=True)


class Review(models.Model):
    content = models.TextField(validators=[validators.MinLengthValidator(10)])
    rating = models.FloatField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    author  = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    article  = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    published_on = models.DateTimeField(editable=False, auto_now_add=True)
