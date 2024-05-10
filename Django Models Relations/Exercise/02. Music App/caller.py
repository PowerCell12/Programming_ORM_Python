import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Song, Artist


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
