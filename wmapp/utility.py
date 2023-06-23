# import
from django.utils import timezone

# Classe Utility

# lista dei generi musicali
list_genres = ["rock", "indie", "classica", "lirica", "metal", "pop", "elettronica"]

# def contains_number
"""
def che ritorna True se la stringa passata come 
parametro contiene un numero, altrimenti False
"""
def contains_number(string):
    return any(char.isdigit() for char in string)

# def pub_past
"""
def che ritorna True se la pubblicazione è 
attuale o passata, altrimenti False
"""
def pub_past(pub):
    # orario attuale
    now = timezone.now()
    # Ritorna True se la data attuale è maggiore o uguale
    # di quella passata come parametro, ovvero quest'ultima
    # è passata e quindi minore rispetto a quella attuale.
    # Ritorna False se la data passata come parametro è successiva,
    # cioè nel futuro, rispetto a quella attuale
    return now >= pub

# def genre_valido
def genre_valido(genretemp):
    # controllo se il genere passato come parametro 
    # si trova nella lista dei generi musicali
    if( genretemp in list_genres ):
        return True
    else:
        return False