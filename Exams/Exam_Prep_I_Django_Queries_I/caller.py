import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count
from main_app.models import Director, Actor, Movie
from statistics import mean


# Import your models here
# Create and run your queries within functions

def get_directors(search_name=None, search_nationality=None):
    all_directors = Director.objects.all()

    if search_name is None and search_nationality is None:
        return ""

    if search_name is None:
        all_directors = all_directors.filter(nationality__icontains=f'{search_nationality}').order_by('full_name')
    elif search_nationality is None:
        all_directors = all_directors.filter(full_name__icontains=f'{search_name}').order_by('full_name')
    else:
        query = Q(full_name__icontains=f'{search_name}') & Q(nationality__icontains=f'{search_nationality}')
        all_directors = all_directors.filter(query).order_by('full_name')


    if not all_directors:
        return ""

    list1 = []

    for directors in all_directors:
        list1.append(f"Director: {directors.full_name}, nationality: {directors.nationality}, experience: {directors.years_of_experience}")

    return '\n'.join(list1)



def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.count_movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(cout_films=Count('movies__id')).order_by('-cout_films', 'full_name').first()

    if not top_actor:
        return ""

    if not top_actor.movies.all():
        return ""


    list1 = []

    for film in top_actor.movies.all():
        list1.append(film.title)

    average = sum([film.rating for film in top_actor.movies.all()]) / len([film for film in top_actor.movies.all()])
    return f"Top Actor: {top_actor.full_name}, starring in movies: {', '.join(list1)}, movies average rating: {average:.1f}"


#
## fix fill database
def fill_database():
    Actor.objects.create(full_name="Tom Cruise", birth_date="1962-07-03", nationality="American", is_awarded=True)
    Actor.objects.create(full_name="Angelina Jolie", birth_date="1975-06-04", nationality="American", is_awarded=True)
    Actor.objects.create(full_name="Tom Hanks", birth_date="1956-07-09", nationality="American", is_awarded=True)
    Actor.objects.create(full_name="Brad Pitt", birth_date="1963-12-18", nationality="American", is_awarded=True)


print(get_top_actor())