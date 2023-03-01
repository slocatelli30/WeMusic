from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=72, null=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'account: {self.user.username}'

class OrdinaryUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    liked_songs = models.ManyToManyField('Song', blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'utente: {self.account.user.username}'

class Artist(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'artista: {self.account.user.username}'

class Album(models.Model):
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.today())

    def __str__(self):
        return self.name

# Song
class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)
    file = models.FileField(upload_to="media")

    def __str__(self):
        return self.title


class Playlist(models.Model):
    creator = models.ForeignKey(OrdinaryUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(
        'creation date', default=datetime.today())
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name
