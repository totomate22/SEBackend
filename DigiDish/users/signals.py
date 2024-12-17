from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):

    if sender.name == 'users':  # Ensure this runs only for your app
        # Define roles and their permissions
        roles_permissions = {
            'Administrator': ['add_user', 'change_user', 'delete_user', 'view_user'],
            'Verwaltung': ['add_user', 'change_user', 'delete_user', 'view_user'],
            'Standortleitung': ['view_user', 'change_user'],
            'Gruppenleitung': ['view_user'],
            'Küchenpersonal': ['view_user'],
        }

        for role_name, permissions in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            group.permissions.clear()  # Clear old permissions
            for permission_codename in permissions:
                permission = Permission.objects.get(codename=permission_codename)
                group.permissions.add(permission)