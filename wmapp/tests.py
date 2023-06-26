"""
Tests.py
"""

# import TestCase
from django.test import TestCase
# import datetime
import datetime
# import timezone
from django.utils import timezone

# import Account
from .models import Account
# import Album
from .models import Album
# import Song
from .models import Song
# import Playlist
from .models import Playlist

class AccountModelTests(TestCase):
    """
    Test per la classe Account
    """

    # test nome account vuoto
    def test_name_account_empty(self):
        """
        Se il nome dell'account riferito ad una persona è vuoto,
        ritorna false in fase di test, altrimenti true
        """
        name_fake = ""
        account_fake = Account(name=name_fake)
        self.assertIs(account_fake.account_name_correct(), False)

    # test nome account contiene numeri
    def test_name_account_number(self):
        """
        Se il nome dell'account riferito ad una persona 
        contiene valori numerici ritorna false in fase di test, 
        altrimenti true
        """
        name_err = "Luca9"
        account_err = Account(name=name_err)
        self.assertIs(account_err.account_name_correct(), False)

    # test email non corretta (pt.1)
    def test_email_account_correct(self):
        """
        Se l'email dell'account riferito ad una persona NON è corretta,
        ritorna false il fase di test
        """
        # email errata per mancanza della @
        email_fake = "pulcinopiowemusic.it"
        account_fake = Account(email=email_fake)
        self.assertIs(account_fake.account_email_correct(), False)

    # test email non corretta (pt.2)
    def test_email_account_correct_2(self):
        """
        Se l'email dell'account riferito ad una persona NON è corretta,
        ritorna false il fase di test
        """
        # email errata per mancanza del punto (.)
        email_fake = "pulcinopio@wemusicit"
        account_fake = Account(email=email_fake)
        self.assertIs(account_fake.account_email_correct(), False)

    # test birth date (corretto)
    def test_birth_date_1(self):
        """
        Se gli anni riferiti ad un account sono corretti,
        ritorna true in fase di test
        """
        # anni corretti
        birth_date_test = datetime.date(1995, 6, 19)
        account_fake = Account(birth_date=birth_date_test)
        self.assertIs(account_fake.account_age_correct(), True)

    # test birth date (non corretto)
    def test_birth_date_2(self):
        """
        Se gli anni riferiti ad un account NON sono corretti,
        ritorna False in fase di test
        """
        # anni corretti
        birth_date_test = datetime.date.today()
        account_fake = Account(birth_date=birth_date_test)
        self.assertIs(account_fake.account_age_correct(), False)

    # test sex (femmina, corretto)
    def test_sex_femmina(self):
        """
        Se il sesso riferito ad un account è corretto,
        ritorna il relativo valore in fase di test
        """
        # sesso corretto
        sex_test = 'F'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexvalue(), 'Femmina')

    # test sex (maschio, corretto)
    def test_sex_maschio(self):
        """
        Se il sesso riferito ad un account è corretto,
        ritorna il relativo valore in fase di test
        """
        # sesso corretto
        sex_test = 'M'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexvalue(), 'Maschio')

    # test sex (non corretto)
    def test_sex_error(self):
        """
        Se il sesso riferito ad un account NON è corretto,
        ritorna False in fase di test
        """
        # sesso corretto
        sex_test = 'bho'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexvalue(), False)

    # test sex (0, corretto)
    def test_sex_0(self):
        """
        Se il sesso riferito ad un account è corretto,
        ritorna il relativo valore boolean in fase di test
        """
        # sesso corretto
        sex_test = 'F'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexbool(), 0)

    # test sex (1, corretto)
    def test_sex_1(self):
        """
        Se il sesso riferito ad un account è corretto,
        ritorna il relativo valore boolean in fase di test
        """
        # sesso corretto
        sex_test = 'M'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexbool(), 1)

    # test sex (NON corretto)
    def test_sex_2(self):
        """
        Se il sesso riferito ad un account è corretto,
        ritorna il relativo valore boolean in fase di test
        """
        # sesso corretto
        sex_test = 'ZZZ'
        account_fake = Account(sex=sex_test)
        self.assertIs(account_fake.sexbool(), False)

class AlbumModelTests(TestCase):
    """
    Test per la classe Album
    """
    # test data pubblicazione corretta
    def test_album_data_pub_correct(self):
        """
        Se la data di pubblicazione dell'album è passata o attuale
        ritorna True, False altrimenti
        """
        # creo una data fantoccia che mi porta nel futuro,
        # tra 30 giorni
        time = timezone.now() + datetime.timedelta(days=30)
        # creo un album futuro
        future_album = Album(pub_date=time)
        # test
        self.assertIs(future_album.album_pub_correct(), False)

class SongModelTests(TestCase):
    """
    Test per la classe Song
    """
    # test genre song corretto (genere inventato)
    def test_song_genre_correct(self):
        """
        Se il genere del brano è valido ritorna False, 
        altrimenti True
        """
        # genere sbagliato, perché inventato
        genre_err = "arabasound"
        genre_err = Song(genre=genre_err)
        self.assertIs(genre_err.song_genre_correct(), False)

    # test genre song corretto (genere corretto)
    def test_song_genre_correct_2(self):
        """
        Se il genere del brano è valido ritorna False, 
        altrimenti True
        """
        # genere corretto
        genre_ok = "lirica"
        genre_ok = Song(genre=genre_ok)
        self.assertIs(genre_ok.song_genre_correct(), True)

    # test year song corretto (numero negativo)
    def test_song_year_corrcet(self):
        """
        Se l'anno del brano è una valore nullo o negativo o
        addirittura non è un int ritorna False, altrimenti True
        """
        # anno sbagliato, perché negativo
        year_err = -23
        song_err = Song(year=year_err)
        self.assertIs(song_err.song_year_correct(), False)

    # test year song corretto (numero con la virgola)
    def test_song_year_corrcet_2(self):
        """
        Se l'anno del brano è una valore nullo o negativo o
        addirittura non è un int ritorna False, altrimenti True
        """
        # anno sbagliato, perché negativo
        year_err = 2000.7
        song_err = Song(year=year_err)
        self.assertIs(song_err.song_year_correct(), False)

class PlaylistModelTests(TestCase):
    """
    Test per la classe Playlist
    """

    # test nome playlist corretto
    def test_playlist_name_correct(self):
        """
        Se il nome della playlist è vuoto,
        ritorna false in fase di test, altrimenti true
        """
        playlist_name_empty = ""
        playlist_err = Playlist(name=playlist_name_empty)
        self.assertIs(playlist_err.playlist_name_correct(), False)

    # test creation date playlist corretto (data futura)
    def test_playlist_creation_date_correct(self):
        """
        Se la data di creazione della Playlist è corretta
        ritorna True, altrimenti False
        """
        # data futura della creazione della Playlist
        playlist_creat_date_err = timezone.now() + datetime.timedelta(days=30)
        # Playlist futura
        playlist_err = Playlist(creation_date=playlist_creat_date_err)
        self.assertIs(playlist_err.playlist_creation_date_correct(), False)

    # test creation date playlist corretto (data passata)
    def test_playlist_creation_date_correct_2(self):
        """
        Se la data di creazione della Playlist è corretta
        ritorna True, altrimenti False
        """
        # data passata della creazione della Playlist
        playlist_creat_date_err = timezone.now() - datetime.timedelta(days=15)
        # Playlist passata
        playlist_err = Playlist(creation_date=playlist_creat_date_err)
        self.assertIs(playlist_err.playlist_creation_date_correct(), True)
