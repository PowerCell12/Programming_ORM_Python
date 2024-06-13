import os
from decimal import Decimal

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




def get_actors_by_movies_count():
    actors = Actor.objects.annotate(count_movies=Count('movie')).order_by('-count_movies', 'full_name')
    list1 = []

    if not actors or actors[0].count_movies == 0:
        return ""



    for i in range(3):

        if i >= len(actors):
            break

        actor = actors[i]
        list1.append(f"{actor.full_name}, participated in {actor.count_movies} movies")

    return '\n'.join(list1)



def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not movie:
        return ""

    starring_actor = movie.starring_actor
    cast = sorted([actor.full_name for actor in movie.actors.all()])


    if starring_actor is None:
        return f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: N/A. Cast: {', '.join(cast)}."

    else:
        return f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {starring_actor.full_name}. Cast: {', '.join(cast)}."



def increase_rating():
    query = Q(is_classic=True) & Q(rating__lt=10)
    to_increase = Movie.objects.filter(query)

    if not to_increase:
        return "No ratings increased."

    count = 0
    for increase in to_increase:
        if increase.rating + Decimal(0.1) <= 10:
            increase.rating += Decimal(0.1)
            increase.save()
            count += 1

    return f"Rating increased for {count} movies."
