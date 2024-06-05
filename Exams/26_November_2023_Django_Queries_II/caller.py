import os
import django
# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg, Max
from main_app.models import Author, Article, Review

# Create and run your queries within functions

def get_authors(search_name=None, search_email=None):

    if search_name == None and search_email == None:
        return ""

    final = Author.objects.all()

    if search_name == None:
        final = final.filter(email__icontains=f"{search_email}")
    elif search_email == None:
        final = final.filter(full_name__icontains=f"{search_name}")
    else:
        final = final.filter(Q(full_name__icontains=f"{search_name}") & Q(email__icontains=f"{search_email}"))

    if not final:
        return ""

    final = final.order_by('-full_name')
    list1 = []

    for thing in final:
        list1.append(f"Author: {thing.full_name}, email: {thing.email}, status: {'Banned' if thing.is_banned else 'Not Banned'}")

    return '\n'.join(list1)



def get_top_publisher():
    final = Author.objects.get_authors_by_article_count().first()

    if not final:
        return ""

    if final.count_articles == 0:
        return ""

    return f"Top Author: {final.full_name} with {final.count_articles} published articles."


def get_top_reviewer():
    final = Author.objects.annotate(count_reviews=Count('review__id')).order_by('-count_reviews', 'email').first()

    if not final:
        return ""

    if final.count_reviews == 0:
        return ""

    return f"Top Reviewer: {final.full_name} with {final.count_reviews} published reviews."



def get_latest_article():

    if not Article.objects.exists():
        return ""

    all = Article.objects.order_by('published_on').last()

    if not all:
        return ""

    all_authors = sorted([thing.full_name for thing in all.authors.all()])
    all_reviews = Review.objects.filter(article=all)
    num_reviews = all_reviews.count()

    if num_reviews == 0:
        avg_rating = 0
    else:
        avg_rating = sum([thing.rating for thing in all_reviews]) / num_reviews

    return f"The latest article is: {all.title}. Authors: {', '.join(all_authors)}. Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    top = Article.objects.annotate(avg=Avg('review__rating'), count=Count('review__id')).filter(count__gt=0).order_by('-avg', 'title').first()

    if not top:
        return ""

    return f"The top-rated article is: {top.title}, with an average rating of {top.avg:.2f}, reviewed {top.count} times."


def ban_author(email=None):

    if not Author.objects.exists():
        return "No authors banned."

    if email == None:
        return "No authors banned."

    try:
        author1 = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."


    author1.is_banned =True
    author1.save()

    all_reviews = Review.objects.filter(author=author1)
    all_reviews_count = all_reviews.count()
    for thing in all_reviews:
        thing.delete()

    return f"Author: {author1.full_name} is banned! {all_reviews_count} reviews deleted."

