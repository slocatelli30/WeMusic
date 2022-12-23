from django.contrib import admin

from .models import Album, Song, Playlist, Artist, OrdinaryUser, Account

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Artist)
admin.site.register(OrdinaryUser)
admin.site.register(Account)
