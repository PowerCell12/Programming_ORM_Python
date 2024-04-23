import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location

# Create queries within functions
def create_pet(name: str, species: str): ## first task
  Pet.objects.create(name=name, species=species)
  return f"{name} is a very cute {species}!"



def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool): ## second task
    Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts(): ## second task
  all_artifacts = Artifact.objects.all()
  all_artifacts.delete()



def show_all_locations(): ## third task
  all_locations = Location.objects.all().order_by("-id") ## maybe wrong
  list1 = []
  for location in all_locations:
    list1.append(f"{location.name} has a population of {location.population}!")

  return "\n".join(list1)


def new_capital(): ## third task
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals(): # third task
  capitals = Location.objects.all().filter(is_capital=True).values('name')
  return capitals



def delete_first_location(): #third task
  first_location = Location.objects.first()
  first_location.delete()
