import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery


# Create and check models

def show_highest_rated_art():
    first_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{first_art.art_name} is the highest-rated art with a {first_art.rating} rating!"


def bulk_create_arts(first_art, second_art):
    list1 = [first_art, second_art]

    ArtworkGallery.objects.bulk_create(list1)



def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()




# Run and print your queries