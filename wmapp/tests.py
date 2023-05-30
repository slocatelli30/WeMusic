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
# import Playlist
from .models import Playlist

# Create your tests here.

# Test per la classe Account
class AccountModelTests(TestCase):
    # test nome account vuoto
    def test_name_account_empty(self):
        """
        Se il nome dell'account riferito ad una persona è vuoto,
        ritorna false in fase di test, altrimenti true
        """
        name_fake = ""
        account_fake = Account(name = name_fake)
        self.assertIs(account_fake.account_name_correct(), False)

    # test nome account contiene numeri
    def test_name_account_number(self):
        """
        Se il nome dell'account riferito ad una persona 
        contiene valori numerici ritorna false in fase di test, 
        altrimenti true
        """
        name_err = "Luca9"
        account_err = Account(name = name_err)
        self.assertIs(account_err.account_name_correct(), False)

    # test email non corretta
    def test_email_account_correct(self):
        """
        Se l'email dell'account riferito ad una persona NON è corretta,
        ritorna false il fase di test
        """
        email_fake = "pulcinopiowemusic.it"
        account_fake = Account(email = email_fake)
        self.assertIs(account_fake.account_email_correct(), False)

# Test per la classe Album
class AlbumModelTests(TestCase):
    # test data pubblicazione corretta
    def test_album_data_pub_correct(self):
        """
        Se la data di pubblicazione dell'album è passata o attuale
        ritorna True, False altrimenti
        """
        # creo una data fantoccia che mi porta nel futuro, 
        # tra 30 giorni
        time = timezone.now() +  datetime.timedelta(days=30)
        # creo un album futuro
        future_album = Album(pub_date = time)
        # test
        self.assertIs(future_album.album_pub_correct(), False)

# Test per la classe Playlist
class PlaylistModelTests(TestCase):
    # test nome playlist corretto
    def test_playlist_name_correct(self):
        """
        Se il nome della playlist è vuoto,
        ritorna false in fase di test, altrimenti true
        """
        playlist_name_empty = ""
        playlist_err = Playlist(name = playlist_name_empty)
        self.assertIs(playlist_err.playlist_name_correct(), False)