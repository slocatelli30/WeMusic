# import datetime
from datetime import datetime
# import User
from django.contrib.auth.models import User
# import models
from django.db import models
# import def contains_number, pub_past, genre_valido into utility.py
from .utility import contains_number, pub_past, genre_valido

# classe Account
class Account(models.Model):

    # opzioni per il sesso dell'utente
    SEX_CHOICES = (
        ('F', 'Femmina'),
        ('M', 'Maschio'),
    )

    # campi (fields)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=72, null=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    # birth date (campo settato a null)
    birth_date = models.DateField(null=True)
    # sesso 
    sex = models.CharField(max_length=7, choices=SEX_CHOICES)

    def __str__(self):
        return f'account: {self.user.username}'
    
    # calcolaEta
    def calcolaEta(self):
        # oggi
        today = datetime.today()
        # return
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    # sexBool (0 = femmina, 1 = maschio)
    def sexBool(self):
        # se femmina, return 0
        if( self.sex == 'F' ):
            return 0
        # altrimenti è maschio, return 1
        else:
            return 1

    # sexValue
    def sexValue(self):
        # se femmina
        if( self.sex == 'F' ):
            # return 0
            return 'Femmina'
        # se maschio
        if( self.sex == 'M' ):
            # return 1
            return 'Maschio'
        else:
            # return null (errore)
            return 'Null'

    # funzione per il controllo dell'email (protezione bassa)
    def account_email_correct(self):
        # condizioni:
        # se l'email dell'account è vuoto oppure
        # se l'email dell'account non contiene la @
        # se l'email dell'account non contiene il .
        if( (not self.email) or 
           ("@" not in self.email) or
           ("." not in self.email) ):
            return False
        else:
            return True
        
    # funzione per il controllo sul nome
    def account_name_correct(self):
        # condizioni:
        # se il nome dell'account è vuoto
        # se il nome dell'account contiene un numero
        if( (not self.name) or
           (contains_number(self.name)) ):
            return False
        else:
            return True

class OrdinaryUser(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    liked_songs = models.ManyToManyField('Song', blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'utente: {self.account.user.username}'

# classe Artist
class Artist(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'artista: {self.account.user.username}'

# classe Album
class Album(models.Model):
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.today())

    def __str__(self):
        return self.name
    
    # funzione per il controllo della pubblicazione dell'album
    def album_pub_correct(self):
        # condizioni:
        # se la pubblicazione dell'album è attuale o passata
        if ( pub_past(self.pub_date) ):
            return True
        else:
            return False

# classe Song
class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artists = models.ManyToManyField(Artist)
    file = models.FileField(upload_to="media")

    def __str__(self):
        return self.title
    
    # funzione per il controllo della 
    # validità di un genere musicale
    def song_genre_correct(self):
        # condizioni:
        # il genere deve essere valido (presente nella lista generi)
        if( genre_valido(self.genre) == True):
            return True
        else:
            return False

    # funzione per il controllo dell'anno
    def song_year_correct(self):
        # condizioni:
        # year non deve essere negativo
        # year deve essere un intero
        if( self.year > 0 and (isinstance(self.year, int)) ):
            return True
        else:
            return False

# classe Playlist
class Playlist(models.Model):
    creator = models.ForeignKey(OrdinaryUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(
        'creation date', default=datetime.today())
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name
    
    # funzione per il controllo del nome della playlist
    def playlist_name_correct(self):
        # condizioni:
        # se il nome della playlist è vuota
        if( not self.name ):
            return False
        else:
            return True
        
    # funzione per il controllo della creazione 
    # della Playlist
    def playlist_creation_date_correct(self):
        # condizioni:
        # se la creazione della Playlist è attuale o passata
        if ( pub_past(self.creation_date) ):
            return True
        else:
            return False