from django.db import models
from django.conf import settings

class Member (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group_id = models.IntegerField(default=0)
    #id is automatically created by django, so no need for extra 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Order(models.Model):
    # Red/blue, extra_salat, etc. as before
    CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
    ]

    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SCANNED = "scanned", "Scanned"
        DELIVERED = "delivered", "Delivered"

    member = models.ForeignKey(
        'Member',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )   
    date = models.DateField()
    choice = models.CharField(max_length=10, choices=CHOICES)
    salat = models.BooleanField(default=False)
    
    # New status field
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('member', 'date')
        ordering = ['date']

    def __str__(self):
        member_name = f"{self.member}" if self.member else "Unassigned"
        return f"Order: {member_name} on {self.date} -> {self.choice}" \
            f" | Salat: {self.salat} | Status: {self.status}"
