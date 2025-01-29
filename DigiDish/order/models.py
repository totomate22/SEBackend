from django.db import models
from django.conf import settings
import os

class Member (models.Model):

    LOCATION_CHOICES = [
    (1, "Location 1"),
    (2, "Location 2"),
    (3, "Location 3")
    ] 

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group_id = models.IntegerField(default=0)
    location = models.IntegerField(choices=LOCATION_CHOICES, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # Field to store QR code

    #id is automatically created by django, so no need for extra 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def generate_qr_code(self):
        import qrcode
        from io import BytesIO
        from django.core.files import File

        pending_orders = self.orders.filter(status='pending')   #get the members orders

       # Generate the QR code content
        qr_content = f"MemberID: {self.id}"

        # Generate the QR code
        qr = qrcode.make(qr_content)

        # Save the QR code to the `qr_code` field
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        qr_file = File(qr_io, name=f"member_{self.id}_qr.png")
        self.qr_code.save(qr_file.name, qr_file)
    

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
