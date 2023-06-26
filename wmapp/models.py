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
    """
    Classe Account
    """

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
        """
        Calcola età
        """

        # oggi
        today = datetime.today()
        # return
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    # sexbool (0 = femmina, 1 = maschio)
    def sexbool(self):
        """
        Valore boolean del sesso dell'utente
        """

        # se femmina, return 0
        if self.sex == 'F':
            return 0
        # se è maschio, return 1
        if self.sex == 'M':
            return 1
        # altrimenti, return False
        return False

    # sexvalue
    def sexvalue(self):
        """
        Valore del sesso dell'utente
        """

        # se femmina
        if self.sex == 'F':
            # return 0
            return 'Femmina'
        # se maschio
        if self.sex == 'M':
            # return 1
            return 'Maschio'
        # return False (errore)
        return False

    # funzione per il controllo dell'email (protezione bassa)
    def account_email_correct(self):
        """
        Funzione per il controllo dell'email (protezione bassa)
        """

        # condizioni:
        # se l'email dell'account è vuoto oppure
        # se l'email dell'account non contiene la @
        # se l'email dell'account non contiene il .
        if ((not self.email) or
           ("@" not in self.email) or
           ("." not in self.email)):
            return False
        # altrimenti
        return True

    # funzione per il controllo sul nome
    def account_name_correct(self):
        """
        Controllo sul nome
        """

        # condizioni:
        # se il nome dell'account è vuoto
        # se il nome dell'account contiene un numero
        if ((not self.name) or
           (contains_number(self.name))):
            return False
        # altrimenti
        return True

    # funzione per il controllo dell'età
    def account_age_correct(self):
        """
        Funzione per il controllo dell'età
        """

        # condizioni:
        # l'età NON deve essere minore di 16 e
        # NON deve superare 100
        if ((self.calcolaEta() >= 16) and (self.calcolaEta() <= 100)):
            return True
        # altrimenti
        return False


class OrdinaryUser(models.Model):
    """
    Classe OrdinaryUser
    """

    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    liked_songs = models.ManyToManyField('Song', blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'utente: {self.account.user.username}'

# classe Artist


class Artist(models.Model):
    """
    Classe Artista
    """

    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'artista: {self.account.user.username}'

# classe Album


class Album(models.Model):
    """
    Classe Album
    """

    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', default=datetime.today())

    def __str__(self):
        return self.name

    # funzione per il controllo della pubblicazione dell'album
    def album_pub_correct(self):
        """
        Funzione per il controllo della pubblicazione dell'album
        """
        # condizioni:
        # se la pubblicazione dell'album è attuale o passata
        if pub_past(self.pub_date):
            return True
        return False

# classe Song


class Song(models.Model):
    """
    Classe Song
    """

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
        """
        Funzione per il controllo della validità di un genere musicale
        """

        # condizioni:
        # il genere deve essere valido (presente nella lista generi)
        if genre_valido(self.genre) is True:
            return True
        return False

    # funzione per il controllo dell'anno
    def song_year_correct(self):
        """
        Funzione per il controllo dell'anno
        """

        # condizioni:
        # year non deve essere negativo
        # year deve essere un intero
        if (self.year > 0 and (isinstance(self.year, int))):
            return True
        # altrimenti
        return False

# classe Playlist


class Playlist(models.Model):
    """
    Classe Playlist
    """

    creator = models.ForeignKey(OrdinaryUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(
        'creation date', default=datetime.today())
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name

    # funzione per il controllo del nome della playlist
    def playlist_name_correct(self):
        """
        Funzione per il controllo del nome della playlist
        """

        # condizioni:
        # se il nome della playlist è vuota
        if not self.name:
            return False
        # altrimenti
        return True

    # funzione per il controllo della creazione
    # della Playlist
    def playlist_creation_date_correct(self):
        """
        Funzione per il controllo della creazione della Playlist
        """

        # condizioni:
        # se la creazione della Playlist è attuale o passata
        if pub_past(self.creation_date):
            return True
        return False
