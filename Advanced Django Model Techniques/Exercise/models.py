from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, EmailValidator, URLValidator, MinLengthValidator
from django.db import models

# Create your models here.

def validate_name(value):

  for thing in value:
    if not (thing.isspace() or thing.isalpha()):
      raise ValidationError("Name can only contain letters and spaces")


def validate_phone_number(value):

  if value[:4] != '+359' or len(value) != 13:
    raise ValidationError("Phone number must start with a '+359' followed by 9 digits")


  for thing in value[1:]:
    try:
      int(thing)
    except ValueError:
      raise ValidationError("Phone number must start with a '+359' followed by 9 digits")



class Customer(models.Model):
  name = models.CharField(max_length=100, validators=[validate_name])
  age = models.PositiveIntegerField(validators=[MinValueValidator(18, "Age must be greater than 18")])
  email = models.EmailField(error_messages={'invalid': 'Enter a valid email address'})
  phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
  website_url = models.URLField(error_messages={'invalid': 'Enter a valid URL'})












class BaseMedia(models.Model):

  class Meta:
    abstract = True
    ordering = ['-created_at', 'title']

  title = models.CharField(max_length=100)
  description = models.TextField()
  genre = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now=True)


class Book(BaseMedia):
  author = models.CharField(max_length=100, validators=[MinLengthValidator(5, "Author must be at least 5 characters long")])
  isbn = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(6, "ISBN must be at least 6 characters long")])

  class Meta(BaseMedia.Meta):
    verbose_name = 'Model Book'
    verbose_name_plural = 'Models of type - Book'

class Movie(BaseMedia):
  director = models.CharField(max_length=100, validators=[MinLengthValidator(8, "Director must be at least 8 characters long")])

  class Meta(BaseMedia.Meta):
    verbose_name = 'Model Movie'
    verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
  artist = models.CharField(max_length=100, validators=[MinLengthValidator(9, "Artist must be at least 9 characters long")])


  class Meta(BaseMedia.Meta):
    verbose_name = 'Model Music'
    verbose_name_plural = 'Models of type - Music'









class Product(models.Model):
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)


  def calculate_tax(self):
    return self.price * Decimal(0.08)

  def calculate_shipping_cost(self, weight: Decimal):
    return weight * Decimal(2.00)

  def format_product_name(self):
    return f"Product: {self.name}"




class DiscountedProduct(Product):

  class Meta:
    proxy =True

  def calculate_price_without_discount(self):
    return self.price * Decimal(1.20)


  def calculate_tax(self):
    return self.price * Decimal(0.05)

  def calculate_shipping_cost(self, weight: Decimal):
    return weight * Decimal(1.50)

  def format_product_name(self):
    return f"Discounted Product: {self.name}"
