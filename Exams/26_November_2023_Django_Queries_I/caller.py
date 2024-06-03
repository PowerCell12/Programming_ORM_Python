import os
import django
# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
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


#
# def pour_data_in_database():
#     # Create some authors
#     Author.objects.create(full_name="John Doe", email="U0Z0A@example.com", is_banned=False, birth_year=1980, website="https://www.johndoe.com")
#     Author.objects.create(full_name="Done John", email="123UOz@example.com", is_banned=True, birth_year=1990, website="https://www.janedoe1.com")
#     Author.objects.create(full_name="Jack Doe", email="X9z2M@example.com", is_banned=False, birth_year=1990, website="https://www.jackdoe2.com")
#     Author.objects.create(full_name="Jane Doe", email="X9z254M@example.com", is_banned=True, birth_year=1990, website="https://www.janedoe2.com")
#
#     #create some Articles
#     Article.objects.create(title="Article 1", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", category="Technology")
#     Article.objects.create(title="Article 2", content="Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", category="Science")
#     Article.objects.create(title="Article 3", content="Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", category="Education")
#     Article.objects.create(title="Article 4", content="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", category="Technology")
#
#     #create some reviews
#     Review.objects.create(content="Great article!", rating=4.5, author=Author.objects.get(full_name="John Doe"), article=Article.objects.get(title="Article 1"))
#     Review.objects.create(content="Excellent reading!", rating=5.0, author=Author.objects.get(full_name="Done John"), article=Article.objects.get(title="Article 2"))
#     Review.objects.create(content="I love it!", rating=4.0, author=Author.objects.get(full_name="Jack Doe"), article=Article.objects.get(title="Article 3"))
#     Review.objects.create(content="I hate it!", rating=1.0, author=Author.objects.get(full_name="Jane Doe"), article=Article.objects.get(title="Article 4"))
