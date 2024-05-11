import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Song, Artist, Product, Review


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



def add_song_to_artist(artist_name: str, song_title: str):
    artis = Artist.objects.filter(name=artist_name).first()
    song = Song.objects.filter(title = song_title).first()

    artis.songs.add(song)


def get_songs_by_artist(artist_name: str):
    all_songs = Song.objects.filter(artists__name = artist_name).order_by('-id')
    return all_songs


def remove_song_from_artist(artist_name: str, song_title: str):
    artis = Artist.objects.filter(name=artist_name).first()
    song = Song.objects.filter(title = song_title).first()

    artis.songs.remove(song)



def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.filter(name=product_name).first()
    all_of_them =  product.reviews.all()
    average = sum(review.rating for review in all_of_them) / len(all_of_them)
    return average


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()