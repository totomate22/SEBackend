from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member

@receiver(post_save, sender=Member)
def generate_member_qr_code(sender, instance, created, **kwargs):
    if created or not instance.qr_code:
        instance.generate_qr_code()