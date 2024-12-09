from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth import authenticate

class User(AbstractBaseUser):
    """
    Benutzer-Modell mit den angegebenen Eigenschaften.
    """

    id = models.CharField(max_length=100, primary_key=True)  # Einfache ID
    username = models.CharField(max_length=150, unique=True)  # Benutzername
    password = models.CharField(max_length=255)  # Passwort
    role = models.CharField(max_length=50, default='user')  # Rolle des Benutzers
    user_data = models.JSONField(default=dict)  # User-spezifische Daten als JSON
    qr_code = models.JSONField(default=list)  # QR-Code als Liste von Listen

    USERNAME_FIELD = 'username'  # Das Feld, das als Benutzername verwendet wird
    REQUIRED_FIELDS = ['id', 'role']  # Notwendige Felder bei der Erstellung

    def __str__(self):
        return self.username

    def login(self, username, password):
        """Authentifizierungsmethode für den Benutzer."""
        user = authenticate(username=username, password=password)
        if user is not None:
            # Benutzer erfolgreich authentifiziert
            return user
        else:
            raise ValueError("Ungültiger Benutzername oder Passwort")

    def log_out(self):
        """Methode zum Abmelden des Benutzers."""
        # In Django erfolgt das Abmelden in der Regel über eine Session-Logik
        # Da dieses Modell keine Session-Verwaltung hat, gehen wir davon aus,
        # dass das Abmelden durch das Löschen der Session oder das Abmelden
        # durch Django selbst erfolgt.
        # Diese Methode könnte erweitert werden, um mit Sessions zu arbeiten.
        print(f"{self.username} wurde abgemeldet.")  # Dies ist ein Platzhalter.
