from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    # Abstract User integriert id, username, first name, last name, email, passwords und haufen booleans
    # Link each user to a role using Django's Group model
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Assign the user to a role (Django Group)."
    )

    def set_role(self, role_name):
        """
        Assign the user to a role (Django Group) based on the role name.
        """
        group, created = Group.objects.get_or_create(name=role_name)
        self.group = group
        self.groups.clear()  # Clear previous roles
        self.groups.add(group)
        self.save()
    
    def __str__(self):
        return self.username

    