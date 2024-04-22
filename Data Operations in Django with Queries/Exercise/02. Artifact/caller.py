import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact

# Create queries within functions
def create_pet(name: str, species: str): ## first task
  Pet.objects.create(name=name, species=species)
  return f"{name} is a very cute {species}!"



def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool): ## second task
    Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts(): ## second task
  all_artifacts = Artifact.objects.all()
  all_artifacts.delete(all_artifacts)
