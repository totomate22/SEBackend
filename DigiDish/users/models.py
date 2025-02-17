from django.contrib.auth.models import AbstractUser
from django.db import models

    
class User(AbstractUser):

    # Location & Role Choices
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

    # Attribute

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    location = models.IntegerField(choices=LOCATION_CHOICES, null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True, default=0)
    is_kitchen = models.BooleanField(default=False)
    

    # Allgemeine Methoden

    def __str__(self):
        return f"{self.username} - {self.role}"
    
    def role_required(self, required_role): #überprüfung ob berechtigt
        if (required_role != self.role):
             raise PermissionError("This method is restricted.")
        return True



    