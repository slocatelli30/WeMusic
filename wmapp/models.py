from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=72)


class OrdinaryUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    liked_songs = models.ManyToManyField('Song')
    friends = models.ManyToManyField('self')


class Artist(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class Album(models.Model):
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.today())


class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)


class Playlist(models.Model):
    creator = models.ForeignKey(OrdinaryUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(
        'creation date', default=datetime.today())
    songs = models.ManyToManyField(Song)
