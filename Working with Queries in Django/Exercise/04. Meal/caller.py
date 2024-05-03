import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal


# Create and check models

def show_highest_rated_art():
    first_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{first_art.art_name} is the highest-rated art with a {first_art.rating} rating!"


def bulk_create_arts(first_art, second_art):
    list1 = [first_art, second_art]

    ArtworkGallery.objects.bulk_create(list1)



def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()



def show_the_most_expensive_laptop():
    most_expensive = Laptop.objects.order_by('-price', '-id').first()
    return f"{most_expensive.brand} is the most expensive laptop available for {most_expensive.price}$!"


def bulk_create_laptops(*args):
    Laptop.objects.bulk_create(*args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand='Asus').update(storage=512)
    Laptop.objects.filter(brand='Lenovo').update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand='Apple').update(memory=16)
    Laptop.objects.filter(brand='Dell').update(memory=16)
    Laptop.objects.filter(brand='Acer').update(memory=16)


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    Laptop.objects.filter(brand='Dell').update(operation_system='Linux')
    Laptop.objects.filter(brand='Acer').update(operation_system='Linux')
    Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')



def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()




## next

def bulk_create_chess_players(*args):
  ChessPlayer.objects.bulk_create(*args)


def delete_chess_players():
  ChessPlayer.objects.filter(title='no title').delete()



def change_chess_games_won():
  ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
  ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
  ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
  ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")


def grand_chess_title_IM():
  ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title="IM")


def grand_chess_title_FM():
  ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title="FM")


def grand_chess_title_regular_player():
  ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title="regular player")



def set_new_chefs():
    Meal.objects.filter(meal_type='Breakfast').update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type='Lunch').update(chef='Julia Child')
    Meal.objects.filter(meal_type='Dinner').update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type='Snack').update(chef='Thomas Keller')



def set_new_preparation_times():
    Meal.objects.filter(meal_type='Breakfast').update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type='Lunch').update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type='Dinner').update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type='Snack').update(preparation_time='5 minutes')


def update_low_calorie_meals():
    Meal.objects.filter(meal_type='Breakfast').update(calories=400)
    Meal.objects.filter(meal_type='Dinner').update(calories=400)



def update_high_calorie_meals():
    Meal.objects.filter(meal_type='Lunch').update(calories=700)
    Meal.objects.filter(meal_type='Snack').update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type='Lunch').delete()
    Meal.objects.filter(meal_type='Snack').delete()

# Run and print your queries