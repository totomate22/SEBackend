from django.contrib.auth.models import AbstractUser
from django.db import models

LOCATION_CHOICES = [
    (1, "Location 1"),
    (2, "Location 2"),
    (3, "Location 3")
]

ROLE_CHOICES = [
    ('verwaltung', 'Verwaltung'),
    ('standortleitung', 'Standortleitung'),
    ('gruppenleitung', 'Gruppenleitung'),
    ('admin', 'Admin')
]
    
class User(AbstractUser):

    # Attribute

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location = models.IntegerField(choices=LOCATION_CHOICES, null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    is_kitchen = models.BooleanField(default=False)

    # Allgemeine Methoden

    def __str__(self):
        return f"{self.username} - {self.role}"
    
    def role_required(self, required_role): #überprüfung ob berechtigt
        if (required_role != self.role):
             raise PermissionError("This method is restricted.")
        return True

    # Methoden für Gruppenleitung

    def create_standortleitung(self, firstname, lastname, password, location=LOCATION_CHOICES):
        gruppenleitung = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            password=password,
            role='gruppenleitung',
            location=location,
            username=f"{firstname.lower()}.{lastname.lower()}"  # username ist bsplw max.mustermann
        )
        gruppenleitung.save()
        return gruppenleitung

    # Methoden für Standortleitung

    def create_standortleitung(self, firstname, lastname, password, location=LOCATION_CHOICES):
        standortleitung = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            password=password,
            role='standortleitung',
            location=location,
            username=f"{firstname.lower()}.{lastname.lower()}"  # username ist bsplw max.mustermann
        )
        standortleitung.save()
        return standortleitung

    # Methoden für Verwaltung

    def create_verwaltung(self, firstname, lastname, password):
        """
        Static method to create a Verwaltung user instance.
        """
        self.role_required('verwaltung') 
        verwaltung = User.objects.create_user( #verwendung von create_user weil passwort dann automatisch gehasht
            first_name=firstname,
            last_name=lastname,
            password=password,
            role='verwaltung',
            username=f"{firstname.lower()}.{lastname.lower()}"  # username ist bsplw max.mustermann
        )
        verwaltung.save()
        return verwaltung


    