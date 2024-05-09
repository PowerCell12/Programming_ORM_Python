import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    Authors = Author.objects.all().order_by('id')
    list1 = []


    for author in Authors:
        if author.book_set.all():
            list1.append(f"{author.name} has written - {', '.join(book.title for book in author.book_set.all())}!")

    return '\n'.join(list1)


def delete_all_authors_without_books() -> None:
    all_authors = Author.objects.all()

    for author in all_authors:
        if not author.book_set.all():
            author.delete()
